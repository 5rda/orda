from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostComment
from .forms import PostForm, PostCommentForm
from django.db.models import Q
from django.conf import settings
import os

# Create your views here.


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    postcomment_form = PostCommentForm()
    postcomments = post.PostComment_set.all()
    context = {
        'post': post,
        'postcomment_form': postcomment_form,
        'postcomments': postcomments,
    }
    return render(request, 'posts/detail.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'posts/create.html', context)


def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user != post.user:
        return redirect('posts:index')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        print(request.FILES)
        if request.FILES.get('image', None) != None:
            image_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
            if os.path.isfile(image_path):
                os.remove(image_path)

        if form.is_valid():
            form.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'posts/update.html', context)


def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        if post.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(post.image1))
            if os.path.isfile(image_path):
                os.remove(image_path)
  
        post.delete()
    return redirect('posts:index')


def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:detail', post.pk)


def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    postcomment_form = PostCommentForm(request.POST)

    if postcomment_form.is_valid():
        postcomment = postcomment_form.save(commit=False)
        postcomment.post = post
        postcomment.user = request.user
        postcomment.save()
        return redirect('posts:detail', post.pk)
    else:
        postcomment_form = PostCommentForm()
    context = {
        'post': post,
        'postcomment_form': postcomment_form,
    }
    return render(request, 'posts/detail.html', context)


def comments_update(request, post_pk, postcomment_pk):
    postcomment = PostComment.objects.get(pk=postcomment_pk)
    
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
        'postcomment_pk': postcomment_pk
    }
    return render(request, 'posts/detail.html', context)


def comments_delete(request, post_pk, postcomment_pk):
    postcomment = PostComment.objects.get(pk=postcomment_pk)
    if request.user == postcomment.user:
        postcomment.delete()
        
    return redirect('posts:detail', post_pk)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()
    context = {
        'posts': posts
    }
    return render(request, 'posts/search.html', context)
