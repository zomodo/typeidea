from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models
from config.models import Link,SlideBar
# Create your views here.

"""
def post_list(request,category_id=None,tag_id=None):
    category=None
    tag=None

    if tag_id:
        try:
            tag=models.Tag.objects.get(id=tag_id)
        except models.Tag.DoesNotExist:
            post_list=[]
        else:
            post_list=tag.post_set.filter(status=models.Post.STATUS_NORMAL)
    else:
        post_list=models.Post.objects.filter(status=models.Post.STATUS_NORMAL)
        if category_id:
            try:
                category=models.Category.objects.get(id=category_id)
            except models.Category.DoesNotExist:
                category=None
            else:
                post_list=post_list.filter(category__id=category_id)

    context={'category':category,'tag':tag,'post_list':post_list}

    return render(request,'blog/list.html',context=context)
"""

def post_list(request,tag_id=None,category_id=None):
    tag=None
    category=None
    if tag_id:
        tag,post_list=models.Post.get_by_tag(tag_id)
    elif category_id:
        category,post_list=models.Post.get_by_category(category_id)
    else:
        post_list=models.Post.latest_post()

    context={'tag':tag,'category':category,'post_list':post_list}
    context.update(models.Category.get_navs())
    context.update({'sidebars':SlideBar.get_all()})
    return render(request,'blog/list.html',context=context)


def post_detail(request,post_id=None):
    try:
        post_detail=models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        post_detail=None

    context={'post_detail':post_detail}
    context.update(models.Category.get_navs())
    context.update({'sidebars':SlideBar.get_all()})
    return render(request,'blog/detail.html',context=context)


