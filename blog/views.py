from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm


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


def post_share(request, post_id):
    """sending posts by mail"""
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # validation form
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # clean form and send e-mail
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'dmtrgrvnk@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})
