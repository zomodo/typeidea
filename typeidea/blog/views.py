from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.db.models import Q   #django提供的条件表达式，用来处理复杂查询
from . import models
from config.models import Link,SlideBar
from comment.models import Comment
# Create your views here.

"""
def post_list(request,category_id=None,tag_id=None):
    category=None
    tag=None

    if tag_id:
        try:
            tag=models.Tag.objects.get(id=tag_id)
        except models.Tag.DoesNotExist:
            post_list=[]
        else:
            post_list=tag.post_set.filter(status=models.Post.STATUS_NORMAL)
    else:
        post_list=models.Post.objects.filter(status=models.Post.STATUS_NORMAL)
        if category_id:
            try:
                category=models.Category.objects.get(id=category_id)
            except models.Category.DoesNotExist:
                category=None
            else:
                post_list=post_list.filter(category__id=category_id)

    context={'category':category,'tag':tag,'post_list':post_list}

    return render(request,'blog/list.html',context=context)
"""

""" 利用function view改造 """
"""
def post_list(request,tag_id=None,category_id=None):
    tag=None
    category=None
    if tag_id:
        tag,post_list=models.Post.get_by_tag(tag_id)
    elif category_id:
        category,post_list=models.Post.get_by_category(category_id)
    else:
        post_list=models.Post.latest_post()

    context={'tag':tag,'category':category,'post_list':post_list}
    context.update(models.Category.get_navs())
    context.update({'sidebars':SlideBar.get_all()})
    return render(request,'blog/list.html',context=context)


def post_detail(request,post_id=None):
    try:
        post_detail=models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        post_detail=None

    context={'post_detail':post_detail}
    context.update(models.Category.get_navs())
    context.update({'sidebars':SlideBar.get_all()})
    return render(request,'blog/detail.html',context=context)
"""

""" 利用class-based view改造 """
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404
from config.models import SlideBar
from comment.forms import CommentForm   # 导入评论中的Form输入框渲染到前端

class CommonViewMixin:      # 顶部导航、底部导航、侧边栏通用数据
    # get_context_data接口：获取渲染到模板中的所有上下文，如果有新增数据需要传递到模板中，可以重写该方法来完成
    def get_context_data(self,**kwargs):
        context=super(CommonViewMixin, self).get_context_data(**kwargs)
        context.update({'sidebars':SlideBar.get_all()})
        context.update(models.Category.get_navs())
        return context

class IndexView(CommonViewMixin,ListView):      # 首页数据
    queryset = models.Post.latest_post()
    paginate_by = 5     # 分页
    context_object_name = 'post_list'       # 设置模板中的变量
    template_name = 'blog/list.html'

class CategoryView(IndexView):      # 分类数据，继承IndexView
    def get_context_data(self, **kwargs):
        context=super(CategoryView, self).get_context_data(**kwargs)
        category_id=self.kwargs.get('category_id')  # self.kwargs中的数据是从URL定义中拿到的
        category=get_object_or_404(models.Category,pk=category_id)
        context.update({'category':category})
        return context

    def get_queryset(self):
        """ 重写queryset，根据分类过滤 """
        queryset=super(CategoryView, self).get_queryset()
        category_id=self.kwargs.get('category_id')
        return queryset.filter(category__id=category_id)

class TagView(IndexView):        # 标签数据，继承IndexView
    def get_context_data(self, **kwargs):
        context=super(TagView, self).get_context_data(**kwargs)
        tag_id=self.kwargs.get('tag_id')
        tag=get_object_or_404(models.Tag,pk=tag_id)
        context.update({'tag':tag})
        return context

    def get_queryset(self):
        """ 重写queryset，根据标签过滤 """
        queryset=super(TagView, self).get_queryset()
        tag_id=self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class PostDetailView(CommonViewMixin,DetailView):   # 文章详情页数据
    queryset = models.Post.latest_post()
    template_name = 'blog/detail.html'
    context_object_name = 'post_detail'
    pk_url_kwarg = 'post_id'

    """
    # 抽象出了评论模块和组件——comment下面的templatetags文件，所以这里要注释掉，
    def get_context_data(self,**kwargs):        # 新增评论数据，并传递到文章明细的模板中
        context=super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            "comment_form":CommentForm,
            "comment_list":Comment.get_by_target(self.request.path),
        })
        return context
    """

class SearchView(IndexView):        # 搜索数据，继承IndexView
    def get_context_data(self,**kwargs):
        context=super(SearchView, self).get_context_data(**kwargs)
        keyword=self.request.GET.get('keyword','') # 获取前端name='keyword'的输入，如果没有数据则为空
        context.update({'keyword':keyword})
        return context

    def get_queryset(self):
        queryset=super(SearchView, self).get_queryset()
        keyword=self.request.GET.get('keyword','')
        if not keyword:
            return queryset
        else:
            return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
            #icontains表示包含，并忽略大小写；| 表示“或”条件

class AuthorView(IndexView):        # 作者过滤，继承IndexView
    def get_queryset(self):
        queryset=super(AuthorView, self).get_queryset()
        author_id=self.kwargs.get('author_id')
        return queryset.filter(owner__id=author_id)

