from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import ListView

from blog.views import CommonViewMixin
from . import models
# Create your views here.

class LinkListView(CommonViewMixin,ListView):   # 友情链接内容
    queryset = models.Link.objects.filter(status=models.Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'