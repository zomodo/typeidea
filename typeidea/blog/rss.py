"""
新建rss文件，利用RSS（简易信息聚合）提供订阅接口，网站有更新时，RSS阅读器会自动获取最新内容，
用户可以在RSS阅读器中看到最新内容，避免每次需要打开网站才能看到是否有更新。
"""
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Post

class ExtendedRSSFeed(Rss201rev2Feed):  # 自定义feed_type实现输出正文部分
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler,item)
        handler.addQuickElement("content:html",item['content_html'])

class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed     # 使用自定义的feed_type
    title_template = "Typeidea Blog System"
    link = "/rss/"
    description_template = "typeidea is a blog system power by django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('detail',args=[item.pk])  # detail是URL中定义的name

    def item_extra_kwargs(self, item):
        return {"content_html":self.item_content_html(item)}

    def item_content_html(self,item):
        return item.content_html        # 这里参见上方handler.addQuickElement
