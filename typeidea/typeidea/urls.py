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
from typeidea.custom_site import custom_site
from blog import views as blog_view
from comment import views as comment_view
from config import views as config_view

urlpatterns = [
    url(r'^super_admin/',admin.site.urls),
    url(r'^admin/', custom_site.urls),
    url(r'^$',blog_view.post_list,name='index'),
    url(r'^category/(?P<category_id>(\d+))/$',blog_view.post_list,name='category'),
    url(r'^tag/(?P<tag_id>(\d+))/$',blog_view.post_list,name='tag'),
    url(r'^post/(?P<post_id>(\d+))/$',blog_view.post_detail,name='detail'),
    url(r'^links/$',config_view.links,name='links'),
]
