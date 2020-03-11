from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache     # 引入缓存，对更新频率不高的数据可以加缓存
import mistune  # 配置Markdown
from django.utils.functional import cached_property
# Create your models here.

class Category(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEMS=[                  # 可列表，可元祖
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    ]

    name=models.CharField(max_length=50,verbose_name='名称')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    is_nav=models.BooleanField(default=False,verbose_name='是否为导航')
    owner=models.ForeignKey(User,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=verbose_name_plural='分类' # verbose_name_plural表示复数形式的显示

    @classmethod
    def get_navs(cls):
        category=cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_category=[]
        normal_category=[]
        for cate in category:
            if cate.is_nav:
                nav_category.append(cate)
            else:
                normal_category.append(cate)
        return {'nav_category':nav_category,'normal_category':normal_category}


class Tag(models.Model):
    STATUS_NORMAL=1     # 这样设置方便views中使用
    STATUS_DELETE=0
    STATUS_ITEMS=[                  # 可列表，可元祖
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    ]

    name=models.CharField(max_length=10,verbose_name='名称')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    owner=models.ForeignKey(User,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=verbose_name_plural='标签' # verbose_name_plural表示复数形式的显示


class Post(models.Model):
    STATUS_NORMAL=1      # 这样设置方便views中使用
    STATUS_DELETE=0
    STATUS_DRAFT=2
    STATUS_ITEMS=[
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
        (STATUS_DRAFT,'草稿'),
    ]

    title=models.CharField(max_length=255,verbose_name='标题')
    desc=models.CharField(max_length=1024,blank=True,verbose_name='摘要')
    content=models.TextField(verbose_name='正文',help_text='正文必须为MarkDown格式')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    category=models.ForeignKey(Category,verbose_name='分类')
    tag=models.ManyToManyField(Tag,verbose_name='标签')
    owner=models.ForeignKey(User,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    pv=models.PositiveIntegerField(default=1)
    uv=models.PositiveIntegerField(default=1)
    content_html=models.TextField(verbose_name='正文html代码',blank=True,editable=False)
    # 文章正文使用Markdown，content_html是用来存储Markdown之后的内容,同时要重写save函数（见下方），editable=False表示不可编辑
    is_md=models.BooleanField(verbose_name='是否Markdown语法',default=False)
    # 新增is_md用于使Markdown和ckeditor共存，修改下文中的save

    def __str__(self):
        return self.title

    class Meta:
        verbose_name=verbose_name_plural='文章'
        ordering=['-id']        # 根据id降序

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag=None
            post_list=[]
        else:
            post_list=tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')

        return tag,post_list

    @staticmethod
    def get_by_category(category_id):
        try:
            category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category=None
            post_list=[]
        else:
            post_list=category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')

        return category,post_list

    @classmethod
    def latest_post(cls,with_related=True):
        # with_related控制返回的数据是否加上两个外键，如果不需要使用owner和category，则在要用的地方加上with_related=False
        queryset=cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('owner','category').prefetch_related('tag')
        return queryset

    # @classmethod
    # def hot_posts(cls):
    #     return cls.objects.filter(status=cls.STATUS_NORMAL).only('id','title').order_by('-pv')

    @classmethod
    def hot_posts(cls):      # 给hot_posts增加缓存,对更新频率不高的数据可以加缓存
        result=cache.get('hot_posts')
        if not result:
            result=cls.objects.filter(status=cls.STATUS_NORMAL).only('id','title').order_by('-pv')
            cache.set('hot_posts',result,10*60)
        return result

    """
    # content_html是用来存储content Markdown之后的内容
    def save(self,*args,**kwargs):  
        self.content_html=mistune.markdown(self.content)
        return super(Post, self).save(*args,**kwargs)
    """
    # 重写save使Markdown和CKeditor共存
    def save(self,*args,**kwargs):
        if self.is_md:
            self.content_html=mistune.markdown(self.content)
        else:
            self.content_html=self.content
        return super(Post, self).save(*args,**kwargs)

    @cached_property
    def tags(self):         # 用作sitemap.xml中的调用
        return ','.join(self.tag.values_list('name',flat=True))
    """
    values_list迭代时返回的是元祖，如果只有一个参数，使用flat=True则表示返回的结果为单个值而不是元祖;
    这里用到django提供的一个工具cached_property，作用是帮我们把返回的数据绑定到实例上，不用每次访问时
    都去执行tags函数中的代码，可对比python内置的property。
    """