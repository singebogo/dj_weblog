import os

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.utils.http import unquote
from article.models import ArticlePost, ArticleColumn
from popular_website.models import PopularWebsite
from .models import Jmxs
from .forms import FileUploadModelForm


# Show file list
def file_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    files = Jmxs.objects.all()

    # 搜索查询集
    if search:
        files = files.filter(
            Q(file__icontains=search) |
            Q(desc__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        files = files.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        files = files.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'id':
        files = files.order_by("-id")

    paginator = Paginator(files, 15)
    page = request.GET.get('page')
    files = paginator.get_page(page)

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 最新文章
    article_latest_list = article_list[:10]

    # 获取分类
    categories = ArticleColumn.objects.all()
    # 常用网站
    popularWebsite_list = PopularWebsite.objects.all()
    # 最热文章
    article_hot_list = article_list.order_by('-total_views')[:10]
    return render(request, 'jmx_list.html', {'files': files, "article_latest_list": article_latest_list,
                                             "article_hot_list": article_hot_list,
                                             "categories": categories,
                                             'websites': popularWebsite_list, })


def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        context = {'form': form, 'heading': 'Upload files with Regular Form'}
        if form.is_valid():
            form.save()  # 一句话足以
            return redirect(reverse("jmxs:file_list"))
    else:
        form = FileUploadModelForm()
        # 初始化查询集
        article_list = ArticlePost.objects.all()

        # 最新文章
        article_latest_list = article_list[:10]

        # 获取分类
        categories = ArticleColumn.objects.all()
        # 常用网站
        popularWebsite_list = PopularWebsite.objects.all()
        # 最热文章
        article_hot_list = article_list.order_by('-total_views')[:10]
        context = {'form': form, 'heading': 'Upload files with ModelForm',
                   "article_latest_list": article_latest_list,
                   "article_hot_list": article_hot_list,
                   "categories": categories,
                   'websites': popularWebsite_list,
                   }

    return render(request, 'jmx_upload_form.html', context=context)


def download_file(request, pk):
    try:
        myfile = Jmxs.objects.get(id=pk)
        file_path = myfile.file.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=unquote(os.path.basename(file_path)))
            # response["content_type"] = "application/octet-stream"
            # response['Content-Disposition'] = "attachment;filename={}".format(
            #     unquote(os.path.basename(file_path)))  # 字符串替换成下载文件
            return response
        else:
            return HttpResponse('文件不存在！')
    except Exception as e:
        return HttpResponse('文件不存在！')


def delete_file(request, id):
    # 通过id查找到文件，删除存储文件及数据库中记录
    myfile = Jmxs.objects.get(id=id)
    os.remove(myfile.file.path)
    myfile.delete()
    return redirect(reverse("jmxs:file_list"))
