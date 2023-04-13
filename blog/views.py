from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)

from .models import Post


def post_list(request):
    """render list of posts"""
    post_list = Post.published.all()
    # add pagination
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number not integer
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number out of range
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    """render object by id OR http404"""
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
