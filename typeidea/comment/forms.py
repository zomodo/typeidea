from django import forms
import mistune
from . import models

class CommentForm(forms.ModelForm):
    nickname=forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={"class":"form-control","style":"width:60%;"}
        )
    )
    email=forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={"class":"form-control","style":"width:60%;"}
        )
    )
    website=forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={"class":"form-control","style":"width:60%;"}
        )
    )
    content=forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={"class":"form-control","rows":6,"cols":60}
        )
    )
    # 上面可以直接用widget=forms.aaa 或者widget=forms.widgets.aaa

    def clean_content(self):
        content=self.cleaned_data['content']  # 或者这样写self.cleaned_data.get('content')
        if len(content)<10:
            raise forms.ValidationError('内容长度怎么能这么短呢！')
        content=mistune.markdown(content)
        # 配置Markdown，配置之后HTML代码将直接展示在页面上，这时需要在前端content上下增加{% autoescape off %}{{  }}{% endautoescape %}
        return content

    class Meta:
        model=models.Comment
        fields=['nickname','email','website','content']
