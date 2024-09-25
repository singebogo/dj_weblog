from django import forms

from article.models import ArticleColumn
from .models import Jmxs


# 写文章的表单类
class FileUploadModelForm(forms.ModelForm):
    column = forms.ModelChoiceField(
        queryset=ArticleColumn.objects.all(),
        label="*文件类型:",
        required=True,
        initial='',
        # choices=MyIntervalSchedule.PERIOD_CHOICES,
        widget=forms.Select(
            attrs={"class": "form-control selectpicker", "placeholder": "请选择文件类型"})
    )
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        # 指明数据模型来源
        model = Jmxs
        # 定义表单包含的字段
        fields = ('column', 'tags', 'file', 'desc')
