from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from article.models import ArticlePost, ArticleColumn
from popular_website.models import PopularWebsite


class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    login_url = '/userprofile/login/'
    
    paginate_by = 20  # if pagination is desired

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 初始化查询集
        article_list = ArticlePost.objects.all()

        # 最新文章
        context["article_latest_list"] = article_list[:10]

        # 获取分类
        context["categories"] = ArticleColumn.objects.all()
        # 常用网站
        context["websites"] = PopularWebsite.objects.all()
        # 最热文章
        context["article_hot_list"] = article_list.order_by('-total_views')[:10]
        return context


class CommentNoticeUpdateView(View):
    """更新通知状态"""
    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')