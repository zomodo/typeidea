"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page    # 引入缓存模块
import xadmin
from rest_framework.routers import DefaultRouter    # 配置api的url
from rest_framework.documentation import include_docs_urls

from typeidea.custom_site import custom_site
from blog import views as blog_view
from comment import views as comment_view
from config import views as config_view
from blog.rss import LatestPostFeed     # 订阅接口
from blog.sitemap import PostSitemap       # 站点地图
from typeidea.autocomplete import CategoryAutocomplete,TagAutocomplete
# from blog.apis import post_list,PostList
from blog.apis import PostViewSet,CategoryViewSet,TagViewSet   # api

"""
urlpatterns = [
    url(r'^super_admin/',admin.site.urls),
    url(r'^admin/', custom_site.urls),
    url(r'^$',blog_view.post_list,name='index'),
    url(r'^category/(?P<category_id>(\d+))/$',blog_view.post_list,name='category'),
    url(r'^tag/(?P<tag_id>(\d+))/$',blog_view.post_list,name='tag'),
    url(r'^post/(?P<post_id>(\d+))/$',blog_view.post_detail,name='detail'),
    url(r'^links/$',config_view.links,name='links'),
]
"""
router=DefaultRouter()
router.register(r'post',PostViewSet)             # 注册文章api的url
router.register(r'category',CategoryViewSet)     # 注册分类api的url
router.register(r'tag',TagViewSet)               # 注册标签api的url


# 利用class-based view改造之后的URL
urlpatterns = [
    # url(r'^super_admin/',admin.site.urls),  # xadmin不支持多个site配置
    # url(r'^admin/', custom_site.urls),      # xadmin不支持多个site配置
    url(r'^admin/',xadmin.site.urls,name='xadmin'),
    url(r'^$',blog_view.IndexView.as_view(),name='index'),
    url(r'^category/(?P<category_id>(\d+))/$',blog_view.CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<tag_id>(\d+))/$',blog_view.TagView.as_view(),name='tag'),
    url(r'^post/(?P<post_id>(\d+)).html$',blog_view.PostDetailView.as_view(),name='detail'),
    url(r'^links/$',config_view.LinkListView.as_view(),name='links'),
    url(r'^search/$',blog_view.SearchView.as_view(),name='search'),
    url(r'^author/(?P<author_id>(\d+))/$',blog_view.AuthorView.as_view(),name='author'),
    url(r'^comment/$',comment_view.CommentView.as_view(),name='comment'),
    url(r'^rss|feed/',LatestPostFeed(),name='rss'),     # 订阅接口，|表示或
    # url(r'^sitemap.xml$',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),   # 站点地图
    # 上面是正常的站点地图配置，下面是加了缓存之后的站点地图配置，20分钟内django会直接读取缓存中的数据
    url(r'^sitemap.xml$',cache_page(60*20,key_prefix='sitemap_cache_')(sitemap_views.sitemap),{'sitemaps':{'posts':PostSitemap}}),
    # category和tag的autocomplete配置url
    url(r'^category_autocomplete/$',CategoryAutocomplete.as_view(),name='category_autocomplete'),
    url(r'^tag_autocomplete/$',TagAutocomplete.as_view(),name='tag_autocomplete'),
    url(r'^ckeditor/',include('ckeditor_uploader.urls')),   # ckeditor配置图片上传
    # url(r'^api/post/',PostList.as_view(),name='post-list'),
    # url(r'^api/post/',post_list,name='post-list'),
    url(r'^api/',include(router.urls)), # api
    url(r'^api/docs/',include_docs_urls(title='typeidea apis')),    # api文档

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)    # 配置图片上传路径

# 意思是当DEBUG=True时候引入django-debug-toolbar的debug_toolbar，并配置对应的URL地址
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/',include(debug_toolbar.urls)),
    ]