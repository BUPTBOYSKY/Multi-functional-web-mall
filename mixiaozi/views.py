from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
import os
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse  
import json  
from .models import CartItem,Product,FaceImage  
import logging
from .models import Product, ProductDetail
from django.http import HttpResponseServerError
import re
import oss2
import uuid
from django.conf import settings
import requests
import sys
import subprocess
import os
import numpy as np
import time
from .models import UserProfile

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'mixiaozi/home.html')

def digital_view(request):
    return render(request, 'mixiaozi/3c_digital.html')

def clothing_view(request):
    return render(request, 'mixiaozi/clothing.html')

def supermarket_view(request):
    return render(request, 'mixiaozi/supermarket.html')

def cart_view(request):
    return render(request, 'mixiaozi/chart.html')

def messages_view(request):
    return render(request, 'mixiaozi/messages.html')

def member_view(request):
    return render(request, 'mixiaozi/huiyuan.html')

def xiaomi14pro_view(request):
    return render(request, 'mixiaozi/xiaomi14pro.html')

def RNW_view(request):
    return render(request, 'mixiaozi/RNW.html')

def yilimilk_view(request):
    return render(request, 'mixiaozi/yilimilk.html')

def gane_1_view(request):
    return render(request, 'mixiaozi/gane_1.html')

def ok_view(request):
    return render(request, 'mixiaozi/ok.html')

def face_register(request):
    return render(request, 'mixiaozi/face_register.html')

def face_re_register_page(request):
    return render(request, 'mixiaozi/face_re_register.html')

from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms import RegisterForm, LoginForm

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, '两次输入的密码不一致')
                return redirect('register')

            hashed_password = make_password(password)

            if User.objects.filter(username=username).exists():
                messages.error(request, '用户名已存在')
            else:
                user = User.objects.create(username=username, password=hashed_password)

                UserProfile.objects.create(user=user)

                messages.success(request, '注册成功！请登录。')
                return redirect('login')

    return render(request, 'mixiaozi/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print(f"Attempting to authenticate user: {username}")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("Authentication successful")
                login(request, user)

                # 增加用户积分
                profile = UserProfile.objects.get(user=user)
                profile.points += 1
                profile.save()

                messages.success(request, '登录成功')

                next_url = request.POST.get('next', 'cart')
                return redirect(next_url)
            else:
                print("Authentication failed")
                messages.error(request, '用户名或密码错误')
        else:
            print("Form is not valid:", form.errors)
            messages.error(request, '表单无效，请检查输入。')

    else:
        form = LoginForm()

    # 获取 next_url，保证即使出错也有一个默认值
    next_url = request.GET.get('next', '')

    return render(request, 'mixiaozi/login.html', {'form': form, 'next': next_url})


def facelogin_view(request):
    if request.method == 'POST':
        image_data = request.POST.get('imageData')

        if image_data:
            try:
                image_data = image_data.split(',')[1]
                image_binary = base64.b64decode(image_data)
                image_path = os.path.join('static', 'uploaded_images', 'captured_image.jpg')
                with open(image_path, 'wb') as f:
                    f.write(image_binary)
                messages.success(request, '人脸识别成功，登录成功！')
                return redirect('home')
            except Exception as e:
                messages.error(request, '处理图像时发生错误，请重试。')
        else:
            messages.error(request, '未能捕获图像，请重试。')

    return render(request, 'mixiaozi/facelogin.html')

def save_image_to_db(request):
    if request.method == 'POST':
        image_data = request.POST.get('imageData')

        if not image_data:
            messages.error(request, 'No image data found, please try again.')
            print('No image data received')
            return JsonResponse({'success': False, 'message': 'No image data found, please try again.'})

        try:
            image_data = image_data.split(',')[1]
            image_binary = base64.b64decode(image_data)
            file_path = 'C:/Users/86157/Desktop/Django_test/myproject/yoloV3-deepface-exe/data/test_img/faceimagetemp_image.jpg'

            with open(file_path, 'wb') as f:
                f.write(image_binary)

            result_file_path = r'C:\Users\86157\Desktop\Django_test\myproject\yoloV3-deepface-exe\result\document.txt'

            start_time = time.time()
            timeout = 120 

            while not os.path.exists(result_file_path):
                if time.time() - start_time > timeout:
                    return JsonResponse({'success': False, 'message': 'Face recognition failed, please try again.'})
                time.sleep(0.5) 

            with open(result_file_path, 'r') as result_file:
                result_content = result_file.read().strip()

            if not result_content.startswith('Recognition result:'):
                return JsonResponse({'success': False, 'message': 'Invalid format in recognition result file.'})

            user_id = result_content.split(':')[1].strip()

            os.remove(result_file_path)

            User = get_user_model()
            try:
                user = User.objects.get(username=user_id)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                # 增加用户积分
                profile = UserProfile.objects.get(user=user)
                profile.points += 1
                profile.save()

                messages.success(request, f"欢迎，{user.username}！人脸识别成功。")
                return JsonResponse({'success': True, 'user_id': user.username, 'message': 'Face recognition successful.'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found in the system.'})

        except Exception as e:
            messages.error(request, f"Error processing image: {str(e)}")
            print(f"Exception occurred: {e}")
            return JsonResponse({'success': False, 'message': f"Error processing image: {str(e)}"})

    return render(request, 'mixiaozi/home.html')


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        for item in cart_items:
            item.subtotal = item.product.price * item.quantity
    else:
        cart_items = []
        total_price = 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'mixiaozi/chart.html', context)

@csrf_exempt
@login_required
def update_cart_item(request):
    if request.method == 'POST':
        logger.info('收到更新购物车的POST请求')
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            action = data.get('action')

            item = CartItem.objects.get(id=item_id, user=request.user)
            if action == 'add':
                item.quantity += 1
            elif action == 'reduce' and item.quantity > 1:
                item.quantity -= 1
            else:
                return JsonResponse({'success': False, 'error': '无效的操作或数量'}, status=400)

            item.save()

            updated_price = item.product.price * item.quantity
            total_price = sum(i.product.price * i.quantity for i in CartItem.objects.filter(user=request.user))
            return JsonResponse({
                'success': True,
                'quantity': item.quantity,
                'updated_price': updated_price,
                'total_price': total_price
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': '商品未找到'}, status=404)

    return JsonResponse({'success': False, 'error': '无效请求'}, status=400)


@csrf_exempt
@login_required
def delete_cart_item(request):
    if request.method == 'POST':
        logger.info('收到删除购物车的POST请求')
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            item = CartItem.objects.get(id=item_id, user=request.user)
            item.delete()
            total_price = sum(i.product.price * i.quantity for i in CartItem.objects.filter(user=request.user))
            return JsonResponse({'success': True, 'total_price': total_price})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        user = request.user

        try:
            product = Product.objects.get(id=product_id)
            print(f"Product found: {product}")
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})

        try:
            cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

            print(f"CartItem: {cart_item}, Created: {created}")

            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error while adding to cart: {e}")
            return JsonResponse({'success': False, 'error': 'Error while adding to cart'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def digital_view(request):
    products = Product.objects.filter(category='3c_digital')
    context = {'products': products}
    return render(request, 'mixiaozi/3c_digital.html', context)


import random
import string
def save_face_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        image_data = request.POST.get('imageData')

        # 检查必填字段是否为空
        if not username or not password or not image_data:
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        try:
            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists.'})

            # 解析图片数据
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_bytes = base64.b64decode(imgstr)

            # 创建用户并保存密码
            hashed_password = make_password(password)
            user = User.objects.create(username=username, password=hashed_password)

            # 创建用户的 UserProfile 并初始化积分为 0
            UserProfile.objects.create(user=user, points=0)

            # 将图片存储在特定路径下，使用用户名作为文件名
            save_path = r'C:\Users\86157\Desktop\Django_test\myproject\yoloV3-deepface-exe\data\base_face'
            file_name = f"{username}.{ext}"
            file_path = os.path.join(save_path, file_name)
            with open(file_path, 'wb') as f:
                f.write(image_bytes)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error saving image: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy('home'))

def save_face_re_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        image_data = request.POST.get('imageData')

        # 检查必填字段是否为空
        if not username or not password or not image_data:
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        try:
            # 检查用户是否存在
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User does not exist.'})

            # 检查密码是否正确
            if not check_password(password, user.password):
                return JsonResponse({'success': False, 'message': 'Incorrect password.'})

            # 解析图片数据
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_bytes = base64.b64decode(imgstr)

            # 将图片存储在特定路径下，使用用户名作为文件名
            save_path = r'C:\Users\86157\Desktop\Django_test\myproject\yoloV3-deepface-exe\data\base_face'
            file_name = f"{username}.{ext}"
            file_path = os.path.join(save_path, file_name)
            with open(file_path, 'wb') as f:
                f.write(image_bytes)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error saving image: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_detail = getattr(product, 'details', None)
    return render(request, 'mixiaozi/product_detail.html', {
        'product': product,
        'product_detail': product_detail
    })

def clothing_view(request):
    products = Product.objects.filter(category='clothing')
    context = {'products': products}
    return render(request, 'mixiaozi/clothing.html', context)

def supermarket_view(request):
    products = Product.objects.filter(category='supermarket')
    context = {'products': products}
    return render(request, 'mixiaozi/supermarket.html', context)