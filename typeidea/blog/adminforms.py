# Author : zmd
# Date : 2019/12/27 17:34
# Desc : 这是用作后台管理的form，不是前台针对用户输入进行处理的form，要区分开;

from django import forms

class PostAdminForm(forms.ModelForm):
    desc=forms.CharField(widget=forms.Textarea,label='摘要',required=True)