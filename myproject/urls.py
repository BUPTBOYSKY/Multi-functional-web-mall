from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理后台
    path('mixiaozi/', include('mixiaozi.urls')),  # 注册 mixiaozi 应用的 URL
]

# 添加如下代码来配置媒体文件的 URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)