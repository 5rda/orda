from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostComment
from .forms import PostForm, PostCommentForm
from django.db.models import Q, Count
from django.conf import settings
from bs4 import BeautifulSoup
from django.http import JsonResponse
import os
from django.http import JsonResponse
from mountains.models import Mountain


# Create your views here.


def index(request):
    query = request.GET.get('q')
    search_option = request.GET.get('search_option')

    view_posts = Post.objects.order_by('-view_count')
    like_posts = Post.objects.annotate(like_count=Count('like_users')).order_by('-like_count')

    if query and search_option:
        if search_option == 'title':
            filtered_posts = Post.objects.filter(title__contains=query)
        elif search_option == 'author':
            filtered_posts = Post.objects.filter(user__nickname__contains=query)
        elif search_option == 'content':
            filtered_posts = Post.objects.filter(content__contains=query)
        elif search_option == 'title_content':
            filtered_posts = Post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
    else:
        filtered_posts = Post.objects.order_by('-created_at')

    context = {
        'view_posts': view_posts,
        'like_posts': like_posts,
        'posts': filtered_posts,
        'query': query,
    }

    if query:
        return render(request, 'posts/search.html', context)
    else:
        return render(request, 'posts/index.html', context)


def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    postcomment_form = PostCommentForm()
    postcomments = post.postcomment_set.order_by('-id')

    prev_posts = Post.objects.filter(pk__lt=post_pk).order_by('-pk')[:2]
    next_posts = Post.objects.filter(pk__gt=post_pk).order_by('pk')[:2]
    posts = list(prev_posts)  + list(next_posts)
    session_key = f'post_viewed_{post_pk}'

    if not request.session.get(session_key):
        post.view_count += 1
        post.save()
        request.session[session_key] = True

    context = {
        'post': post,
        'postcomment_form': postcomment_form,
        'postcomments': postcomments,
        'posts': posts,
    }
    return render(request, 'posts/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.mountain = Mountain.objects.get(pk=request.POST.get('mountain'))
            post.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()

    context = {
        'form': form,
        'mountains': Mountain.objects.all(),
    }
    return render(request, 'posts/create.html', context)


@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user != post.user:
        return redirect('posts:index')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.mountain = form.cleaned_data['mountain']
            post.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm(instance=post, initial={'mountain': post.mountain})

    context = {
        'post': post,
        'form': form,
        'mountains': Mountain.objects.all(),
    }
    return render(request, 'posts/update.html', context)


def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
  
        post.delete()
    return redirect('posts:index')


@login_required
def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked':is_liked,
        'like_count':post.like_users.count()
    }
    return JsonResponse(context)
    # return redirect('posts:detail', post.pk)


@login_required
def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    postcomment_form = PostCommentForm(request.POST)

    if postcomment_form.is_valid():
        postcomment = postcomment_form.save(commit=False)
        postcomment.post = post
        postcomment.user = request.user
        postcomment.save()
        # return redirect('posts:detail', post.pk)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': postcomment_form.errors})
    #     postcomment_form = PostCommentForm()
    # context = {
    #     'post': post,
    #     'postcomment_form': postcomment_form,
    # }
    # return render(request, 'posts/detail.html', context)


@login_required
def comment_update(request, post_pk, comment_pk):
    postcomment = PostComment.objects.get(pk=comment_pk)

    if request.method == 'POST':
        form = PostCommentForm(request.POST, instance=postcomment)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post_pk)
    else:
        form = PostCommentForm(instance=postcomment)

    context = {
        'form': form,
        'post_pk': post_pk,
        'comment_pk': comment_pk
    }
    return render(request, 'posts/comment_update.html', context)


@login_required
def comment_delete(request, post_pk, comment_pk):
    postcomment = PostComment.objects.get(pk=comment_pk)
    if request.user == postcomment.user:
        postcomment.delete()
        post_comments = PostComment.objects.filter(post=post_pk).count()
        return JsonResponse({'status': 'ok','post_comments': post_comments})
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})
    # return redirect('posts:detail', post_pk)


@login_required
def comment_likes(request, post_pk, comment_pk):
    comment = PostComment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
        cl_is_liked = False
    else:
        comment.like_users.add(request.user)
        cl_is_liked = True
    cl_likes_count = comment.like_users.all().count()
    context = {
        'cl_is_liked' : cl_is_liked,
        'cl_likes_count' : cl_likes_count,
    }
    return JsonResponse(context)
    # return redirect('posts:detail', post_pk)


@login_required
def comment_dislikes(request, post_pk, comment_pk):
    comment = PostComment.objects.get(pk=comment_pk)
    if comment.dislike_users.filter(pk=request.user.pk).exists():
        comment.dislike_users.remove(request.user)
        cd_is_liked = False
    else:
        comment.dislike_users.add(request.user)
        cd_is_liked = True
    cd_likes_count = comment.dislike_users.all().count()
    context = {
        'cd_is_liked' : cd_is_liked,
        'cd_likes_count' : cd_likes_count,
    }
    return JsonResponse(context)
    # return redirect('posts:detail', post_pk)


def search(request):
    query = request.GET.get('q')
    search_option = request.GET.get('search_option')

    view_posts = Post.objects.order_by('-view_count')
    like_posts = Post.objects.annotate(like_count=Count('like_users')).order_by('-like_count')

    if query and search_option:
        if search_option == 'title':
            filtered_posts = Post.objects.filter(title__contains=query)
        elif search_option == 'author':
            filtered_posts = Post.objects.filter(user__nickname__contains=query)
        elif search_option == 'content':
            filtered_posts = Post.objects.filter(content__contains=query)
        elif search_option == 'title_content':
            filtered_posts = Post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
    else:
        filtered_posts = Post.objects.order_by('-created_at')

    context = {
        'view_posts': view_posts,
        'like_posts': like_posts,
        'posts': filtered_posts,
        'query': query,
        'search_option': search_option,
    }

    return render(request, 'posts/search.html', context)


def proofshot(request):
    image_posts = Post.objects.filter(content__icontains='<img').order_by('-created_at')
    
    context = {
        'image_posts': image_posts,
    }

    return render(request, 'posts/proofshot.html', context)


def get_first_image_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    if img_tag:
        return img_tag['src']
    else:
        return None
    