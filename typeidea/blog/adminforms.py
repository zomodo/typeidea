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
        widget=CKEditorWidget(),
        label='正文',
        required=True,
    )
    """

    # content添加富文本编辑器，可以添加图片
    # 修改content使Markdown和CKeditor共存，所以注释掉
    # content=forms.CharField(
    #     widget=CKEditorUploadingWidget(),
    #     label='正文',
    #     required=True,
    # )

    # 以下全部是配置Markdown和CKeditor共存的内容，建议直接使用一种方法CKeditor，即上方配置

    content_ck=forms.CharField(
        widget=CKEditorUploadingWidget(),
        label='正文',
        required=False,
    )
    content_md=forms.CharField(
        widget=forms.Textarea(),
        label='正文',
        required=False,
    )
    content=forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model=Post
        fields=(
            'category','tag','title','desc','status',
            'is_md','content','content_ck','content_md'
        )

    # 使Markdown和CKeditor共存
    def __init__(self,instance=None,initial=None,**kwargs):
        initial=initial or {}
        if instance:
            if instance.is_md:
                initial['content_md']=instance.content
            else:
                initial['content_ck']=instance.content
        super(PostAdminForm, self).__init__(instance=instance,initial=initial,**kwargs)

    def clean(self):
        is_md=self.cleaned_data['is_md']
        if is_md:
            content_field_name='content_md'
        else:
            content_field_name='content_ck'

        content=self.cleaned_data[content_field_name]
        if not content:
            self.add_error(content_field_name,'必填项！')
            return
        self.cleaned_data['content']=content
        return super(PostAdminForm, self).clean()

    class Media:
        js=('js/post_editor.js',)

