"""
抽象出一个基类BaseOwnerAdmin,完成两件事：一是重写save方法，设置对象的owner；二是重写get_queryset方法，只显示当前用户的数据
"""
from django.contrib import admin
class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来针对queryset过滤当前用户的数据，这里设置为如果是超级用户就展示所有数据，否则只展示当前用户的数据
    2.用来自动补充文章，分类，标签，侧边栏，友链这些models的owner字段
    """
    exclude = ('owner',)

    def get_queryset(self, request):
        qs=super(BaseOwnerAdmin, self).get_queryset(request)
        # 先对用户进行判断，如果是超级用户就展示所有数据，如果不是，则只展示当前用户的数据
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(BaseOwnerAdmin, self).save_model(request,obj,form,change)

"""
下面需要做的是，要改造哪些需要隔离不同用户数据的页面，就把对应的admin类继承这个基类即可
在这里需要把blog/admin文件中的admin.ModelAdmin改成BaseOwnerAdmin
"""