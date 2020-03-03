# 创建serializers.py文件，是用来序列化数据的地方,需要为不同的接口定义不同的serializer
# PostSerializer中可以自定义字段，自定义检验逻辑，自定义数据处理理逻辑
from rest_framework import serializers,pagination

from.models import Post,Category,Tag


class PostSerializer(serializers.ModelSerializer):  # 文章列表接口
    category=serializers.SlugRelatedField(          # 外键数据需要用SlugRelatedField配置
        read_only=True,                             # 定义是否可写
        slug_field='name',                          # 指定要展示的字段
    )
    tag=serializers.SlugRelatedField(
        many=True,                                  # 多对多需要配置many=True
        read_only=True,
        slug_field='name',
    )
    owner=serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    created_time=serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S'
    )

    class Meta:
        model=Post
        fields=['id','title','category','tag','owner','created_time']

class PostDetailSerializer(PostSerializer):    # 文章详情接口，继承PostSerializer
    class Meta:
        model=Post
        fields=['id','title','category','tag','owner','content_html','created_time']


class CategorySerializer(serializers.ModelSerializer):  # 分类列表接口
    class Meta:
        model=Category
        fields=['id','name','created_time']

class CategoryDetailSerializer(CategorySerializer):    # 分类详情接口，获取分类下的文章列表，继承上方
    posts=serializers.SerializerMethodField('category_paginated_posts')

    def category_paginated_posts(self,obj):
        posts=obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator=pagination.PageNumberPagination()
        page=paginator.paginate_queryset(posts,self.context['request'])
        serializer=PostSerializer(page,many=True,context={'request':self.context['request']})
        return {
            'count':posts.count(),
            'results':serializer.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
        }

    class Meta:
        model=Category
        fields=['id','name','created_time','posts']
"""
SerializerMethodField作用是帮我们把posts字段获取的内容映射到category_paginated_posts方法上，
也就是在最终返回的数据中，posts对应的数据需要通过category_paginated_posts来获取；
category_paginated_posts中实现了对分类下的文章列表获取和分页，并返回分页信息
"""

class TagSerializer(serializers.ModelSerializer):       # 标签列表接口
    class Meta:
        model=Tag
        fields=['id','name','created_time']

class TagDetailSerializer(TagSerializer):       # 标签详情接口，获取标签下的文章列表，继承上方
    posts=serializers.SerializerMethodField('tag_paginated_posts')

    def tag_paginated_posts(self,obj):
        posts=obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator=pagination.PageNumberPagination()
        page=paginator.paginate_queryset(posts,self.context['request'])
        serializer=PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model=Tag
        fields=['id','name','created_time','posts']