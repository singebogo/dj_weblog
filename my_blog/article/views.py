from django.shortcuts import render, HttpResponse
import markdown
# 引入redirect重定向模块
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.detail import View

from .models import ArticlePost, ArticleColumn
from comment.models import Comment
from comment.forms import CommentForm
from popular_website.models import PopularWebsite


# 视图函数
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 最新文章
    article_latest_list = article_list[:10]

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 获取分类
    categories = ArticleColumn.objects.all()

    # 最热文章
    article_hot_list = ArticlePost.objects.all()
    article_hot_list = article_hot_list.order_by('-total_views')
    article_hot_list = article_hot_list[:10]

    # 常用网站
    popularWebsite_list = PopularWebsite.objects.all()

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        "categories": categories,
        'websites': popularWebsite_list,
        'tag': tag,
        "article_latest_list": article_latest_list,
        "article_hot_list": article_hot_list,

    }

    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    # article = ArticlePost.objects.get(id=id)
    article = get_object_or_404(ArticlePost, id=id)

    # 过滤出所有的id比当前文章小的文章
    pre_article = ArticlePost.objects.filter(id__lt=article.id).order_by('-id')
    # 过滤出id大的文章
    next_article = ArticlePost.objects.filter(id__gt=article.id).order_by('id')

    # 取出相邻前一篇文章
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    # 取出相邻后一篇文章
    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None

    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 常用网站
    popularWebsite_list = PopularWebsite.objects.all()

    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 引入评论表单
    comment_form = CommentForm()

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 最新文章
    article_latest_list = article_list[:10]

    # 获取分类
    categories = ArticleColumn.objects.all()

    # 最热文章
    article_hot_list = article_list.order_by('-total_views')[:10]

    # 添加comments上下文
    context = {'article': article, 'toc': md.toc, 'comments': comments, 'comment_form': comment_form,
               'pre_article': pre_article,
               'next_article': next_article,
               "article_latest_list": article_latest_list,
               "article_hot_list": article_hot_list,
               "categories": categories,
               'websites': popularWebsite_list,
               }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 增加 request.FILES
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            # 指定目前登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()

            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()

            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        # 初始化查询集
        article_list = ArticlePost.objects.all()

        # 最新文章
        article_latest_list = article_list[:10]

        # 获取分类
        categories = ArticleColumn.objects.all()

        # 最热文章
        article_hot_list = article_list.order_by('-total_views')[:10]

        # 常用网站
        popularWebsite_list = PopularWebsite.objects.all()
        # 赋值上下文
        context = {
            'article_post_form': article_post_form,
            "article_latest_list": article_latest_list,
            "article_hot_list": article_hot_list,
            'websites': popularWebsite_list,
            "categories": categories, }
        # 返回模板
        return render(request, 'article/create.html', context)


# 删文章
def article_safe_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST, instance=article)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            article_post_form.instance.author = request.user
            article_post_form.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm(instance=article)
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        # 初始化查询集
        article_list = ArticlePost.objects.all()

        # 最新文章
        article_latest_list = article_list[:10]

        # 获取分类
        categories = ArticleColumn.objects.all()

        # 最热文章
        article_hot_list = article_list.order_by('-total_views')[:10]

        # 常用网站
        popularWebsite_list = PopularWebsite.objects.all()

        context = {'article_post': article, 'article_post_form': article_post_form,
                   "article_latest_list": article_latest_list,
                   "article_hot_list": article_hot_list,
                   'websites': popularWebsite_list,
                   "categories": categories, }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
