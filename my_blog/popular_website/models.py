from django.db import models
from django.contrib.auth.models import User


# 常用网站
class PopularWebsite(models.Model):
    name = models.CharField(verbose_name="名称", max_length=200, blank=False, null=False, help_text="网站名称")
    url = models.URLField(verbose_name="地址", max_length=200, blank=False, null=False, help_text="网站地址")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='websites'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        unique_together = ["name", "url", "user"]

    def __str__(self):
        return self.name
