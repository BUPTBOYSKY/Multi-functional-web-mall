from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('3c_digital/', views.digital_view, name='3c_digital'),
    path('clothing/', views.clothing_view, name='clothing'),
    path('supermarket/', views.supermarket_view, name='supermarket'),
    path('cart/', views.cart_view, name='cart'),
    path('messages/', views.messages_view, name='messages'),
    path('member/', views.member_view, name='member'),
    path('xiaomi14pro/', views.xiaomi14pro_view, name='xiaomi14pro'),
    path('RNW/', views.RNW_view, name='RNW'),
    path('yilimilk/', views.yilimilk_view, name='yilimilk'),
    path('ok/', views.ok_view, name='ok'),
    path('facelogin/', views.facelogin_view, name='facelogin'),
    path('gane_1/', views.gane_1_view, name='gane_1'),
    path('save_image_to_db/', views.save_image_to_db, name='save_image_to_db'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('xiaomi14pro/<int:product_id>/', views.xiaomi14pro_view, name='xiaomi14pro'),
    path('face_register/', views.face_register, name='face_register'),
    path('save_face_registration/', views.save_face_registration, name='save_face_registration'),
    path('logout/', views.custom_logout, name='logout'),
    path('face_re_register/', views.face_re_register_page, name='face_re_register'),
    path('save_face_re_register/', views.save_face_re_register, name='save_face_re_register'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='mixiaozi/login.html'), name='login'),
]


