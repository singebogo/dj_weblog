# 引入path
from django.urls import path
from .views import *
# 正在部署的应用的名称
app_name = 'article'


urlpatterns = [
    # home
    path('', article_list, name='home'),
    # 文章列表
    path('article-list/', article_list, name='article_list'),
    # 文章详情
    path('article-detail/<int:id>/', article_detail, name='article_detail'),
    # 写文章
    path('article-create/', article_create, name='article_create'),
    # 安全删除文章
    path('article-safe-delete/<int:id>/', article_safe_delete,  name='article_safe_delete'),
    # 更新文章
    path('article-update/<int:id>/', article_update, name='article_update'),
    # 点赞 +1
    path(
        'increase-likes/<int:id>/',
        IncreaseLikesView.as_view(),
        name='increase_likes'
    ),
]