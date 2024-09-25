from django.db import models
from taggit.managers import TaggableManager

from article.models import ArticleColumn


class Jmxs(models.Model):
    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='jmxs'
    )
    # 文章标签
    tags = TaggableManager(blank=True, help_text="A comma-separated list of tags. 多个标签之间使用英文逗号隔开")
    file = models.FileField(upload_to='jmx/', blank=True, null=True, max_length=100, verbose_name='文件地址',
                            help_text="文件名称地址")
    desc = models.CharField(verbose_name="描述", blank=True, null=True, max_length=100, help_text='文件描述')
