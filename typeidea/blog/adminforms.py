# Author : zmd
# Date : 2019/12/27 17:34
# Desc : 这是用作后台管理的form，不是前台针对用户输入进行处理的form，要区分开;

from django import forms
from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post,Tag,Category
# 引入了django-autocomplete-light之后继续配置category和tag的展示逻辑

class PostAdminForm(forms.ModelForm):
    desc=forms.CharField(widget=forms.Textarea,label='摘要',required=True)

    category=forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category_autocomplete'),
        label='分类',
    )
    tag=forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag_autocomplete'),
        label='标签',
    )

    """
    # content添加富文本编辑器，不能添加图片
    content=forms.CharField(
        widget=CKEditorWidget,
        label='正文',
        required=True,
    )
    """

    # content添加富文本编辑器，可以添加图片
    content=forms.CharField(
        widget=CKEditorUploadingWidget,
        label='正文',
        required=True,
    )


    class Meta:
        model=Post
        fields=['category','tag','title','desc','content','status']