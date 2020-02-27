"""
抽象出一个基类BaseOwnerAdmin,完成两件事：一是重写save方法，设置对象的owner；二是重写get_queryset方法，只显示当前用户的数据
"""

"""
# admin方式
from django.contrib import admin
class BaseOwnerAdmin(admin.ModelAdmin):
    '''
    1.用来针对queryset过滤当前用户的数据，这里设置为如果是超级用户就展示所有数据，否则只展示当前用户的数据
    2.用来自动补充文章，分类，标签，侧边栏，友链这些models的owner字段
    '''
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

'''
下面需要做的是，要改造哪些需要隔离不同用户数据的页面，就把对应的admin类继承这个基类即可
在这里需要把blog/admin文件中的admin.ModelAdmin改成BaseOwnerAdmin
'''

"""

# xadmin方式
class BaseOwnerAdmin:   # 引入了xadmin之后，继承改为object或者去掉
    '''
    1.用来针对queryset过滤当前用户的数据，这里设置为如果是超级用户就展示所有数据，否则只展示当前用户的数据
    2.用来自动补充文章，分类，标签，侧边栏，友链这些models的owner字段
    get_queryset(self, request)
    变为：get_list_queryset(self)
    save_model(self, request, obj, form, change)
    变为：save_models(self)
    '''
    exclude = ('owner',)

    def get_list_queryset(self):
        request=self.request
        qs=super(BaseOwnerAdmin, self).get_list_queryset()
        # 先对用户进行判断，如果是超级用户就展示所有数据，如果不是，则只展示当前用户的数据
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(owner=request.user)

    def save_models(self):
        self.new_obj.owner=self.request.user
        return super(BaseOwnerAdmin, self).save_models()
