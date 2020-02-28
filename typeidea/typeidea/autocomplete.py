# 新建autocomplete，用来配置所有需要自动补全的接口，可以把这个模块理解为自动补全的view层

from dal import autocomplete

from blog.models import Post,Tag,Category

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:  # 判断是否登录
            return Category.objects.none()  # 返回空的queryset

        qs=Category.objects.filter(owner=self.request.user)
        if self.q:
            qs=qs.filter(name__istartswith=self.q)

        return qs

class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:  # 判断是否登录
            return Tag.objects.none()   # 返回空的queryset

        qs=Tag.objects.filter(owner=self.request.user)
        if self.q:
            qs=qs.filter(name__istartswith=self.q)

        return qs

"""
get_queryset作用是处理数据源；get_queryset中判断用户是否登录，
如果未登录返回空的queryset，因为最后结果还会被其他模块处理，所以不能直接返回None值；
接着获取该用户创建的标签和分类；
最后判断是否存在self.q，这里的q就是url参数上传递过来的值，再使用name__istartswith进行查询
"""


