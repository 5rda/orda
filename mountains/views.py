from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.gis.serializers.geojson import Serializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
import json, os
from django.db.models import F, Count, When, Case
from django.conf import settings
from .forms import ReviewCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.


class MountainListView(ListView):
    template_name = 'mountains/mountain_list.html'
    context_object_name = 'mountains'
    model = Mountain
    paginate_by = 10

    def get_queryset(self):
        sort_option = self.request.GET.get('sort', 'likes')  # 기본값으로 가나다순을 사용

        if sort_option == 'likes':
            queryset = Mountain.objects.order_by('-likes')  # 좋아요순으로 정렬
        elif sort_option == 'reviews':
            queryset = Mountain.objects.order_by('-reviews_count')  # 리뷰 개수순으로 정렬
        elif sort_option == 'id':
            queryset = Mountain.objects.order_by('id')  # 가나다순으로 정렬
        elif sort_option == 'views':
            queryset = Mountain.objects.order_by('-views')  # 조회순으로 정렬
        elif sort_option == 'height':
            queryset = Mountain.objects.order_by('height') # 고도순으로 정렬
        else:
            queryset = Mountain.objects.all()  # 기본적으로 모든 데이터 조회

        return queryset


class MountainDetailView(DetailView):
    template_name = 'mountains/mountain_detail.html'
    context_object_name = 'mountain'
    model = Mountain

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        Mountain.objects.filter(pk=self.object.pk).update(views=F('views') + 1)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mountain = self.get_object()
        serializer = Serializer()
        courses = mountain.course_set.all()
        course_details = {}
        for course in courses:
            geojson_data = serializer.serialize(CourseDetail.objects.filter(crs_name_detail=course), fields=('geom', 'is_waypoint', 'waypoint_name', 'crs_name_detail'))
            course_details[course.pk] =geojson_data
        context = {
            'mountain': mountain,
            'courses': courses,
            'course_details': course_details,
            'form': ReviewCreationForm()
        }
        # json_data = json.dumps(course_details, indent=4, sort_keys=True, ensure_ascii=False)
        # file_path = os.path.join(settings.STATICFILES_DIRS[0], 'course_details2.json')
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     file.write(json_data)
        return context


class CourseListView(ListView):
    template_name = 'mountains/course_list.html'
    context_object_name = 'courses'
    model = Course
    paginate_by = 5    

    def get_queryset(self):
        mountain_pk = self.kwargs['mountain_pk']
        mountain = Mountain.objects.get(pk=mountain_pk)
        sort_option = self.request.GET.get('sort', '')  # 정렬 옵션 가져오기

        queryset = Course.objects.filter(mntn_name=mountain)

        if sort_option == 'bookmarks':
            queryset = queryset.annotate(num_bookmarks=Count('bookmarks')).order_by('-num_bookmarks')
        elif sort_option == 'distance':
            queryset = queryset.order_by('distance')
        elif sort_option == 'hidden_time':
            queryset = queryset.order_by('hidden_time')
        elif sort_option == 'diff':
            # 난이도 정렬을 추가
            queryset = queryset.annotate(
                diff_order=Case(
                    When(diff='하', then=1),
                    When(diff='중', then=2),
                    When(diff='상', then=3),
                    default=4
                )
            ).order_by('diff_order')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mountain_pk = self.kwargs['mountain_pk']
        courses = self.get_queryset()
        mountain = Mountain.objects.get(pk=mountain_pk)
        sort_option = self.request.GET.get('sort', '')  # 정렬 옵션 가져오기

        serializer = Serializer()
        course_details = {}
        for course in courses:
            geojson_data = serializer.serialize(CourseDetail.objects.filter(crs_name_detail=course), fields=('geom', 'is_waypoint', 'waypoint_name', 'crs_name_detail'))
            course_details[course.pk] =geojson_data
        context = {
            'mountain': mountain,
            'courses': courses,
            'course_details': course_details
        }        
        return context        


class CourseAllListView(ListView):
    template_name = 'mountains/course_all_list.html'
    context_object_name = 'courses'
    model = Course

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_option = self.request.GET.get('sort', '')  # 기본값으로 전체

        if sort_option == 'bookmarks':
            queryset = queryset.annotate(bookmarks_count=Count('bookmarks'))
            queryset = queryset.order_by('-bookmarks_count')

        return queryset


def mountain_likes(request, mountain_pk):
    mountain = get_object_or_404(Mountain, pk=mountain_pk)
    user = request.user
    if user in mountain.likes.all():
        mountain.likes.remove(user)
        is_liked = False
    else:
        mountain.likes.add(user)
        is_liked = True

    return JsonResponse({'is_liked': is_liked})    


def bookmark(request, mountain_pk, course_pk):
    mountain = get_object_or_404(Mountain, pk=mountain_pk)
    course = get_object_or_404(Course, pk=course_pk)
    user = request.user
    if course in user.bookmarks.all():
        user.bookmarks.remove(course)
        is_bookmarked = False
    else:
        user.bookmarks.add(course)
        is_bookmarked = True
    context = {
        'is_bookmarked' : is_bookmarked,
    }
    return JsonResponse(context)


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

            return redirect('mountains:review_detail', mountain.pk, review.pk)
    else:
        form = ReviewCreationForm()
    context = {
        'form': form,
        'mountain': mountain,
    }
    return render(request, 'mountains/create_review.html', context)


@login_required
def review_likes(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return redirect('mountains:review_detail', pk, review.pk)


# class MountainTestView(ListView):
#     model = Mountain
#     template_name = 'mountains/mountain_test.html'
#     context_object_name = 'mountains'
    

@login_required
def review_delete(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.user == request.user:
        review.delete()
        return redirect('mountains:mountain_detail', pk)
    

def review_detail(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    tags = review.tags.all()
    form = ReviewCreationForm(instance=review)
    context = {
        'review': review,
        'tags': tags,
        'form': form,
    }
    return render(request, 'mountains/review_detail.html', context)


@login_required
def review_update(request, pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewCreationForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                form.save()
                return redirect('mountains:review_detail', review.mountain.pk, review.pk)
        else:
            form = ReviewCreationForm(instance=review)
    else:
        return JsonResponse({'success': True})
    context = {
        'form': form,
        'review': review,
    }
    return JsonResponse({'success': True})