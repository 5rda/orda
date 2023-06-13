from mountains.models import *
from mountains.forms import ReviewCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def create_review(request, pk):
    mountain = Mountain.objects.get(pk=pk)

    if request.method == 'POST':
        form = ReviewCreationForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.mountain = mountain
            review.user = request.user
            review.save()
            form.save_m2m()

            return redirect('mountains:mountain_detail', pk)
    else:
        form = ReviewCreationForm()
    context = {
        'form': form,
        'pk': pk,
    }
    return render(request, 'mountains/mountain_detail.html', context)


@login_required
def review_likes(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        rl_is_liked = False
    else:
        review.like_users.add(request.user)
        rl_is_liked = True
    rl_likes_count = review.like_users.all().count()
    context = {
        'rl_is_liked' : rl_is_liked,
        'rl_likes_count' : rl_likes_count,
    }
    return JsonResponse(context)


@login_required
def review_delete(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
        return redirect('mountains:mountain_detail', pk)
    

@login_required
def review_update(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewCreationForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                return redirect('mountains:mountain_detail', review.mountain.pk)
        else:
            form = ReviewCreationForm(instance=review)
    else:
        return JsonResponse({'message': '해당 리뷰를 작성한 유저가 아닙니다.'})
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'mountains/review_update.html', context)


@login_required
def review_image_delete(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        if request.method == 'POST':
            review.image.delete(save=True)
            return redirect('mountains:review_update', pk, review_pk)
    else:
        return JsonResponse({'error': '권한이 없습니다.'})