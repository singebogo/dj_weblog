from django.utils import timezone
from django.utils.http import unquote
import math, os

from django import template
register = template.Library()

@register.filter(name='transfer')
def transfer(value, arg):
    """将输出强制转换为字符串 arg """
    return arg

@register.filter()
def lower(value):
    """将字符串转换为小写字符"""
    return value.lower()

@register.filter()
def baseName(value):
    """获取文件名称"""
    return unquote(os.path.basename(value))


@register.filter()
def unQuote(value):
    """中文转义"""
    return unquote(value)

# 获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"