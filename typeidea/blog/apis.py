# apis.py是Serializers的View层逻辑

"""
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view()
def post_list(request):
    posts=Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers=PostSerializer(posts,many=True)
    return Response(post_serializers.data)

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
"""

"""
上面的代码跟之前编写的function view和class-based view很相似：
1.api_view是django-rest-framework用来帮我们把一个View转化成API View的装饰器，
提供可选参数api_view(['GET','POST'])来限定请求的类型；

2.ListCreateAPIView跟前面的ListView很相似，我们只需要指定queryset，配置好用来
序列化的类serializer_class = PostSerializer就可以实现一个数据列表页；

3.django-rest-framework中还提供了ListAPIView，区别是：
ListCreateAPIView包含了create功能，能够接受POST请求；
ListAPIView是指单纯的输出列表，只支持GET请求。
"""
# 上面是测试的，单个数据接口,只有列表接口，没有详情页接口

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post,Category,Tag
from .serializers import PostSerializer,PostDetailSerializer
from .serializers import CategorySerializer,CategoryDetailSerializer
from .serializers import TagSerializer,TagDetailSerializer

# 这里用viewsets.ReadOnlyModelViewSet创建只读接口;viewsets.ModelViewSet是可读可写的接口
class PostViewSet(viewsets.ReadOnlyModelViewSet):     # 文章列表api和文章详情api的view层
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer       # 文章列表接口的serializer
    # permission_classes = [IsAdminUser]      # 写入时的权限校验

    # 重写获取详情数据的接口retrieve，列表接口和详情接口对应不同的serializer
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=PostDetailSerializer   # 文章详情接口的serializer
        return super(PostViewSet, self).retrieve(request,*args,**kwargs)

"""
/api/post/ 访问api文章列表页
/api/post/<post_id>/ 访问api文章详情页
"""

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):   # 分类列表api和分类详情api的view层
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = CategorySerializer       # 分类列表接口的serializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=CategoryDetailSerializer  # 分类详情接口的serializer
        return super(CategoryViewSet, self).retrieve(request,*args,**kwargs)

"""
/api/category/ 访问api分类列表页
/api/category/<category_id>/ 访问api分类详情页
"""

class TagViewSet(viewsets.ReadOnlyModelViewSet):       # 标签列表api和标签详情api的view层
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)
    serializer_class = TagSerializer        # 标签列表接口的serializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class=TagDetailSerializer       # 标签详情接口的serializer
        return super(TagViewSet, self).retrieve(request,*args,**kwargs)

"""
/api/tag/ 访问api标签列表页
/api/tag/<tag_id>/ 访问api标签详情页
"""