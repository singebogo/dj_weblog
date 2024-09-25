"""
URL configuration for my_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
import notifications.urls
from django.views.static import serve # 导入媒体文件资源


def return_static(request, path, insecure=True, **kwargs):
  return serve(request, path, insecure, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('article/', include('article.urls', namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),

    path('password-reset/', include('password_reset.urls')),
    # 评论
    path('comment/', include('comment.urls', namespace='comment')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # notice
    path('notice/', include('notice.urls', namespace='notice')),
    # side
    path('side/', include('side.urls', namespace='side')),

    path('accounts/', include('allauth.urls')),
    path('tools/', include('tools.urls')),    
    path('jmxs/', include('jmxs.urls')),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),  # ckeditor上传路由分发
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'files/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # # 图片文件路径，这里要注意，之前已经在setting.py文件处设置了媒体文件路径的别名是：MEDIA_URL = "/files/" ，所以这里的路由要保持一致
    # re_path(r'^static/(?P<path>.*)$', return_static, name='static'), # 添加这行
    re_path(r'^(?!media).*$', include('article.urls')),
]
# 添加这行
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
