from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """render list of posts"""
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, id):
    """render object by id OR http404"""
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
