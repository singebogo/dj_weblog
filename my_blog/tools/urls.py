from django.urls import path, re_path
from . import views

app_name = 'tools'

urlpatterns = [
    # View File List
    path('', views.file_list, name='file_list'),
    path('file/', views.file_list, name='file_list'),
    # Upload File Without Using Model Form
    re_path(r'^upload1/$', views.file_upload, name='file_upload'),
    # Upload Files Using Model Form
    re_path(r'^upload2/$', views.model_form_upload, name='model_form_upload'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    path("delete/<int:id>", views.delete_file, name='delete_file'),
]