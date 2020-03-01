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
import xadmin

from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static

from typeidea.custom_site import custom_site
from blog import views as blog_view
from comment import views as comment_view
from config import views as config_view
from blog.rss import LatestPostFeed     # 订阅接口
from blog.sitemap import PostSitemap       # 站点地图
from typeidea.autocomplete import CategoryAutocomplete,TagAutocomplete


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
    url(r'^rss|feed/',LatestPostFeed(),name='rss'),
    url(r'^sitemap\.xml$',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),
    # category和tag的autocomplete配置url
    url(r'^category_autocomplete/$',CategoryAutocomplete.as_view(),name='category_autocomplete'),
    url(r'^tag_autocomplete/$',TagAutocomplete.as_view(),name='tag_autocomplete'),
    url(r'^ckeditor/',include('ckeditor_uploader.urls')),   # ckeditor配置图片上传
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)    # 配置图片上传路径
