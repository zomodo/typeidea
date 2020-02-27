from django.contrib import admin
import xadmin
from .models import Link,SlideBar
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin    # 这里导入一个自定义基类：1.自动补充owner字段 2.queryset过滤当前用户数据
# Register your models here.


# @admin.register(Link,site=custom_site)    # admin
@xadmin.sites.register(Link)        # xadmin
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title','href','status','weight','owner','created_time')
    fields = ('title','href','status','weight')

    # def save_model(self, request, obj, form, change):
    #     obj.owner=request.user
    #     return super(LinkAdmin,self).save_model(request,obj,form,change)

    # 引入了BaseOwnerAdmin基类，无需再重写save_model和get_queryset函数

# @admin.register(SlideBar,site=custom_site)    # admin
@xadmin.sites.register(SlideBar)        # xadmin
class SlideBarAdmin(BaseOwnerAdmin):
    list_display = ('title','display_type','content','status','owner','created_time')
    fields = ('title','display_type','content','status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner=request.user
    #     return super(SlideBarAdmin,self).save_model(request,obj,form,change)

    # 引入了BaseOwnerAdmin基类，无需再重写save_model和get_queryset函数
