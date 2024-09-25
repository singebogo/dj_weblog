from django.db import models
import os
import uuid


# 重命名
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class Tools(models.Model):
    file = models.FileField(upload_to='files/', blank=True, null=True, max_length=100, verbose_name='工具地址', help_text="文件名称地址")
    desc = models.CharField(verbose_name="描述", blank=True, null=True, max_length=100, help_text='文件描述')
