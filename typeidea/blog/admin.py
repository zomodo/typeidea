from django.contrib import admin
from .models import Post,Tag,Category
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','is_nav','owner','created_time','post_count')
    fields = ('name','status','is_nav')

    def save_model(self, request, obj, form, change):       # 重写 save_model函数
        obj.owner=request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)

    def post_count(self,obj):           # 自定义函数-计算不同分类有多少文章
        return obj.post_set.count()
    post_count.short_description = '文章数量'   # 指定表头名称


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category','status','created_time','operator')
    list_display_links = ()
    list_filter = ('category',)
    search_fields = ('title','category__name')
    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True
    fields = (
        ('category','title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self,obj):         # 自定义函数-list_display处增加一列“编辑”
        return format_html(
            "<a href='{}'>编辑</a>",
            reverse("admin:blog_post_change",args=(obj.id,))
        )
    operator.short_description = '操作'       # 指定表头名称

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)

