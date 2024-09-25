from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.conf import settings
from django.utils.http import unquote
from article.models import ArticlePost, ArticleColumn
from popular_website.models import PopularWebsite
from .models import Tools
from .forms import FileUploadForm, FileUploadModelForm
import os
import uuid
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat


# Show file list
def file_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    files = Tools.objects.all().order_by("-id")
    # 搜索查询集
    if search:
        files = files.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
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
        files = files.order_by('-id')

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
    return render(request, 'file_list.html', {'files': files, "article_latest_list": article_latest_list,
                                              "article_hot_list": article_hot_list,
                                              "categories": categories,
                                              'websites': popularWebsite_list, })


# Regular file upload without using ModelForm
def file_upload(request):
    global context
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        context = {'form': form, 'heading': 'Upload files with Regular Form'}
        if form.is_valid():
            # get cleaned data
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")
            new_file = Tools()
            new_file.file = handle_uploaded_file(raw_file)
            new_file.upload_method = upload_method
            new_file.save()
            return redirect(reverse("tools:file_list"))
    else:
        form = FileUploadForm()
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

        context = {'form': form, 'heading': 'Upload files with Regular Form',
                   "article_latest_list": article_latest_list,
                   "article_hot_list": article_hot_list,
                   "categories": categories,
                   'websites': popularWebsite_list,
                   }
    return render(request, 'upload_form.html', context=context)


def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join(settings.MEDIA_ROOT, 'files', file_name)  # 获取完整的文件路径

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        context = {'form': form, 'heading': 'Upload files with Regular Form'}
        if form.is_valid():
            form.save()  # 一句话足以
            return redirect(reverse("tools:file_list"))
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

    return render(request, 'upload_form.html', context=context)

def download_file(request, pk):
    try:
        myfile = Tools.objects.get(id=pk)
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
    #通过id查找到文件，删除存储文件及数据库中记录
    myfile = Tools.objects.get(id=id)
    os.remove(myfile.file.path)
    myfile.delete()
    return redirect(reverse("tools:file_list"))