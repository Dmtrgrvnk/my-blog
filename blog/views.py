from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)

from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag


def post_list(request, tag_slug=None):
    """render list of posts"""
    post_list = Post.published.all()
    # add tag to posts for filtering
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # added pagination, 5 objects by one page
    paginator = Paginator(post_list, 5)
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
                  {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    """render object by id OR http404"""
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comments
    comments = post.comments.filter(active=True)
    form = CommentForm()
    # list of similar posts
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


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
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'dmtrgrvnk@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    """render and validation comments"""
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # comment was send
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # bind comment with post
        comment.post = post
        # save comment in db
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


def post_search(request):
    """render and validation search form"""
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # query optimization
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
