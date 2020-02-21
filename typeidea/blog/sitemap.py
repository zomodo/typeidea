"""
sitemap（站点地图）用来描述网站的内容组织结构，其主要用途是提供给搜索引擎，
让它能更好的索引/收录我们的网站。
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'always'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self,obj):
        return obj.created_time

    def location(self, obj):
        return reverse('detail',args=[obj.pk])

"""
items返回所有正常状态的文章；
lastmod返回每篇文章的创建时间；
location返回每篇文章的URL；
写完数据处理的部分后，再编写对应的模板sitemap.xml
"""