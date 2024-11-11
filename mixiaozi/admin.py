from django.contrib import admin
from .models import Product, CartItem  # 导入模型
from .models import Product, ProductDetail
from .models import FaceImage

# 注册模型到 Django Admin 界面
admin.site.register(Product)
admin.site.register(CartItem)

# 删除重复注册的代码
admin.site.unregister(Product)  # 如果之前有重复注册的话

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image']

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'banner_image', 'title', 'price_text', 'description_image']

admin.site.register(FaceImage)
