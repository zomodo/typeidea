from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.

def post_list(request,category_id=None,tag_id=None):
    return render(request,'blog/list.html',{'name':'post_list'})


def post_detail(request,post_id=None):
    return render(request,'blog/detail.html',{'name':'post_detail'})

