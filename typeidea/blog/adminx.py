from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry    # 导入日志相关的模块
import xadmin
from xadmin.layout import Row,Fieldset,Container    # 引入xadmin后导入
from xadmin.filters import manager                  # 引入xadmin的自定义过滤器
from xadmin.filters import RelatedFieldListFilter   # 引入xadmin的自定义过滤器

from .models import Post,Tag,Category
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin  # 这里导入一个自定义基类：1.自动补充owner字段 2.queryset过滤当前用户数据

# Register your models here.

"""
# 继承admin的类
class PostInline(admin.TabularInline):      # stackedinline样式不同,设置在其他页直接编辑 修改文章
    fields = ('title','desc')
    extra = 1   # 控制额外多几个
    model = Post
"""

# 使用xadmin的方式
class PostInline:
    form_layout=(
        Container(
            Row('title','desc'),
        )
    )
    extra = 1   # 控制额外多几个
    model = Post

# @admin.register(Category,site=custom_site)    # admin
@xadmin.sites.register(Category)    # xadmin
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]                 # 在分类页直接编辑/修改文章

    list_display = ('name','status','is_nav','owner','created_time','post_count')
    fields = ('name','status','is_nav')

    # def save_model(self, request, obj, form, change):       # 重写 save_model函数
    #     obj.owner=request.user
    #     return super(CategoryAdmin,self).save_model(request,obj,form,change)

    def post_count(self,obj):           # 自定义函数-计算不同分类有多少文章
        return obj.post_set.count()
    post_count.short_description = '文章数量'   # 指定表头名称

    # def get_queryset(self, request):        # 重写get_queryset函数，当前登陆用户只能看到自己的分类
    #     qs=super(CategoryAdmin,self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # 引入了BaseOwnerAdmin基类，无需再重写save_model和get_queryset函数

# @admin.register(Tag,site=custom_site)    # admin
@xadmin.sites.register(Tag)     # xadmin
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','owner','created_time')
    fields = ('name','status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner=request.user
    #     return super(TagAdmin,self).save_model(request,obj,form,change)

    # 引入了BaseOwnerAdmin基类，无需再重写save_model和get_queryset函数

"""
# admin的自定义过滤器
class CategoryOwnerFilter(admin.SimpleListFilter):
    # 自定义过滤器只展示当前用户分类
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id=self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset
"""
# xadmin的自定义过滤器
class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name=='category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(CategoryOwnerFilter, self).__init__(field,request,params,model,model_admin,field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices=Category.objects.filter(owner=request.user).values_list('id','name')
manager.register(CategoryOwnerFilter,take_priority=True)
"""
test方法的作用是确认字段是否需要被当前的过滤器处理，在方法__init__中，
我们执行完父类__init__之后,又重新定义了self.lookup_choices，这个值在默认情况下查询所有的数据
"""

# @admin.register(Post,site=custom_site)    # admin
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # 引入了自定义的adminforms的PostAdminForm,desc的字段由charfield变成了textarea，这里必须为form
    form = PostAdminForm

    list_display = ('title','category','status','owner','created_time','operator')
    list_display_links = ()
    # list_filter = (CategoryOwnerFilter,)  # admin的自定义过滤器，这里是定义的类名
    list_filter = ('category',)     # xadmin的自定义过滤器，注意这里不是定义的filter类，而是字段名
    search_fields = ('title','category__name')
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True  # 在顶部显示保存功能

    """ 只针对多对多的情况 horizontal：横向、vertical：纵向 """
    filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    exclude = ('owner','pv','uv')        # exclude指定哪些字段不展示
    # fields限定要展示的字段，配置展示字段顺序
    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # fieldsets 控制页面布局
    """ fieldsets中是元祖，元祖中第一个元素是string，第二个元素是dict，而dict的key可以是'fields','description','classes'  """
    """
    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('其他信息',{
            'fields':('tag',),
            'classes':('collapse',),        # collapse标识折叠，或者wide不折叠
        }),
    )
    """
    # xadmin中manytomany字段样式是单排下拉框，需要设置m2m_transfer
    style_fields={'tag':'m2m_transfer'}

    # 修改为xadmin的方式
    form_layout=(
        Fieldset(
            "基础信息",
            Row("title","category"),
            "status",
            "tag",
        ),
        Fieldset(
            "内容信息",
            "desc",
            "content",
        ),
    )

    def operator(self,obj):         # 自定义函数-list_display处增加一列“编辑”
        return format_html(
            "<a href='{}'>编辑</a>",
            # reverse("cus_admin:blog_post_change",args=(obj.id,))    # admin
            # reverse("xadmin:blog_post_change",args=(obj.id,))       # xadmin
            self.model_admin_url('change',obj.id)       # xadmin中更友好的方法
        )
    operator.short_description = '操作'       # 指定表头名称

    # def save_model(self, request, obj, form, change):   # 重写save_model函数，当前owner默认为当前登录用户
    #     obj.owner=request.user
    #     return super(PostAdmin,self).save_model(request,obj,form,change)
    #
    # def get_queryset(self, request):            # 重写get_queryset函数，当前登陆用户只能看到自己的文章
    #     qs=super(PostAdmin,self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # admin中外键下拉框添加过滤，在添加文章时只显示当前用户的分类
    """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='category':
            try:
                obj_id = request.resolver_match.args[0]  # 这里获取当前对象id，非常重要
                kwargs['queryset'] = Category.objects.filter(owner=request.user).exclude(id=int(obj_id))  # 添加过滤条件
            except:
                kwargs['queryset'] = Category.objects.filter(owner=request.user)

        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    """

    # admin中多对多选择框添加过滤，在添加文章时只显示当前用户的标签
    """
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name=='tag':
            try:
                obj_id=request.resolver_match.args[0]
                kwargs['queryset'] = Tag.objects.filter(owner=request.user).exclude(id=int(obj_id))
            except:
                kwargs['queryset'] = Tag.objects.filter(owner=request.user)

        return super(PostAdmin, self).formfield_for_manytomany(db_field,request,**kwargs)
    """
    # xadmin中category外键下拉框添加过滤，tag多对多选择框添加过滤
    # 引入了autocomplete之后，category和tag做了过滤，所以这里去掉，见autocomplete.py
    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     if not self.request.user.is_superuser:
    #         if db_field.name == "category":
    #             kwargs["queryset"] = Category.objects.filter(owner=self.request.user)
    #         if db_field.name == "tag":
    #             kwargs["queryset"] = Tag.objects.filter(owner=self.request.user)
    #
    #     return super().formfield_for_dbfield(db_field,**kwargs)

    # 引入了BaseOwnerAdmin基类，无需再重写save_model和get_queryset函数

    # 可以自定义Media类添加js和css资源，改变后台样式
    # class Media:
    #     css={"all":("https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css",),}
    #     js=("https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.bundle.js",)

    # @property
    # def media(self):
    #     # xadmin基于bootstrap，引入会导致页面样式冲突，这里只做演示
    #     media=super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all':('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
    #     })
    #     return media

"""
# 这里是admin自带的log功能，因为xadmin也自带了log功能，并且默认配置好了展示逻辑，所以这里注释掉
@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):      # 在admin后台查看操作日志

    list_display = ['object_repr','object_id','action_flag','user','change_message']

    def get_queryset(self, request):        # 只显示当前登录用户的日志,admin方式
        qs=super(LogEntryAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
"""


# admin的方式
# admin.site.site_header='Typeidea'
# admin.site.site_title='Typeidea管理后台'
# admin.site.index_title='首页'