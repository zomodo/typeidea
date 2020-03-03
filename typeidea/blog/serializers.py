# 创建serializers.py文件，是用来序列化数据的地方,需要为不同的接口定义不同的serializer
# PostSerializer中可以自定义字段，自定义检验逻辑，自定义数据处理理逻辑
from rest_framework import serializers

from.models import Post


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