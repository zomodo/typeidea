# 创建serializers.py文件，是用来序列化数据的地方
from rest_framework import serializers

from.models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model=Post
        fields=['title','category','desc','content_html','created_time']

# PostSerializer中可以自定义字段，自定义检验逻辑，自定义数据处理理逻辑