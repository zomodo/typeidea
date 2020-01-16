from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Link(models.Model):
    STATUS_ITEMS=[
        (1,'正常'),
        (0,'删除'),
    ]

    title=models.CharField(max_length=50,verbose_name='标题')
    href=models.URLField(verbose_name='链接')     # 默认长度为200
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,verbose_name='状态')
    #   zip打包为元组的列表
    weight=models.PositiveIntegerField(choices=zip(range(1,6),range(1,6)),verbose_name='权重',help_text='权重越高顺序越靠前')
    owner=models.ForeignKey(User,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name=verbose_name_plural='友链'


class SlideBar(models.Model):
    DISPLAY_TYPE_ITEMS=[
        (1,'HTML'),
        (2,'最新文章'),
        (3,'最热文章'),
        (4,'最近评论'),
    ]
    STATUS_SHOW=1
    STATUS_HIDDNE=0
    STATUS_ITEMS=[
        (STATUS_SHOW,'展示'),
        (STATUS_HIDDNE,'隐藏'),
    ]

    title=models.CharField(max_length=50,verbose_name='标题')
    display_type=models.PositiveIntegerField(choices=DISPLAY_TYPE_ITEMS,default=1,verbose_name='展示类型')
    content=models.CharField(max_length=500,blank=True,verbose_name='内容',help_text='如果设置的不为HTML类型，可为空')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    owner=models.ForeignKey(User,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name=verbose_name_plural='侧边栏'

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

