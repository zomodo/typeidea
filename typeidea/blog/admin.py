from django.contrib import admin
from .models import Post,Tag,Category
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
# Register your models here.

class PostInline(admin.TabularInline):      # stackedinline样式不同,设置在其他页直接编辑 修改文章
    fields = ('title','desc')
    extra = 1   # 控制额外多几个
    model = Post

@admin.register(Category,site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline,]                 # 在分类页直接编辑/修改文章

    list_display = ('name','status','is_nav','owner','created_time','post_count')
    fields = ('name','status','is_nav')

    def save_model(self, request, obj, form, change):       # 重写 save_model函数
        obj.owner=request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)

    def post_count(self,obj):           # 自定义函数-计算不同分类有多少文章
        return obj.post_set.count()
    post_count.short_description = '文章数量'   # 指定表头名称

    def get_queryset(self, request):        # 重写get_queryset函数，当前登陆用户只能看到自己的分类
        qs=super(CategoryAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Tag,site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','owner','created_time')
    fields = ('name','status')

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id=self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

@admin.register(Post,site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm        # 引入了自定义的adminforms的PostAdminForm,desc的字段由charfield变成了textarea

    list_display = ('title','category','status','owner','created_time','operator')
    list_display_links = ()
    list_filter = (CategoryOwnerFilter,)
    search_fields = ('title','category__name')
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True  # 在顶部显示保存功能

    """ 只针对多对多的情况 horizontal：横向、vertical：纵向 """
    filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    # exclude = ('owner',)        # exclude指定哪些字段不展示
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
            'classes':('collapse',),
        }),
    )

    def operator(self,obj):         # 自定义函数-list_display处增加一列“编辑”
        return format_html(
            "<a href='{}'>编辑</a>",
            reverse("cus_admin:blog_post_change",args=(obj.id,))
        )
    operator.short_description = '操作'       # 指定表头名称

    def save_model(self, request, obj, form, change):   # 重写save_model函数，当前owner默认为当前登录用户
        obj.owner=request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)

    def get_queryset(self, request):            # 重写get_queryset函数，当前登陆用户只能看到自己的文章
        qs=super(PostAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)

    # 可以自定义Media类添加js和css资源，改变后台样式
    # class Media:
    #     css={"all":("https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css",),}
    #     js=("https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.bundle.js",)

admin.site.site_header='Typeidea'
admin.site.site_title='Typeidea管理后台'
admin.site.index_title='首页'