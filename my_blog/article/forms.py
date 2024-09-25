# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost, ArticleColumn


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    column = forms.ModelChoiceField(
        queryset=ArticleColumn.objects.all(),
        label="*文章类型:",
        required=True,
        initial='',
        # choices=MyIntervalSchedule.PERIOD_CHOICES,
        widget=forms.Select(
            attrs={"class": "form-control selectpicker", "placeholder": "请选择文章类型"})
    )

    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ['id', 'title', 'column', 'body', 'tags', 'avatar']
