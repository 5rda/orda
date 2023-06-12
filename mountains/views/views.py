from mountains.models import *
from mountains.forms import SearchForm
from django.http import JsonResponse
from django.db.models import Count, When, Case, Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.gis.serializers.geojson import Serializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

class SearchView(FormView):
    template_name = 'mountains/search.html'
    form_class = SearchForm
    success_url = 'mountains/mountain_list.html'


def mountain_list(request):
    mountains = Mountain.objects.all()
    if request.method == 'POST':
        tags = request.POST.getlist('tags')
        sido = request.POST.get('sido2')
        gugun = request.POST.get('gugun2')
        search_query = request.POST.get('search_query')
        filter_condition = Q()

        if sido and gugun:
            if ('광역시' in sido) or ('특별시' in sido):
                filter_condition.add(Q(region__contains=sido), filter_condition.AND)
            else:
                if '전체' in gugun:
                    filter_condition.add(Q(region__contains=sido),  filter_condition.AND)
                else:
                    filter_condition.add(Q(region__contains=sido) & Q(region__contains=gugun), filter_condition.AND)

        if tags:
            filtered_mountains = mountains.filter(review__tags__pk__in=tags).annotate(tag_count=Count('review__tags__pk')).order_by('-tag_count')[:3]
            filtered_pks = filtered_mountains.values_list('pk', flat=True)
            mountains = mountains.filter(pk__in=filtered_pks)

        if search_query:
            mountains = mountains.filter(name__icontains=search_query)

        mountains = mountains.filter(filter_condition)

        # 필터링된 객체를 세션에 저장
        request.session['filtered_mountains'] = list(mountains.values_list('pk', flat=True))            

    elif request.method == 'GET':
        # GET 요청 처리
        filtered_pks = request.session.get('filtered_mountains', [])
        if filtered_pks:
            mountains = Mountain.objects.filter(pk__in=filtered_pks)
        else:
            mountains = Mountain.objects.all()
        sort = request.GET.get('sort', None)
            
        if sort== 'likes':
            mountains = mountains.annotate(likes_count=Count('likes')).order_by('-likes_count')  # 좋아요순으로 정렬
        elif sort == 'reviews':
            mountains = mountains.annotate(reviews_count2=Count('review')).order_by('-reviews_count2') 
        elif sort == 'id':
            mountains = mountains.order_by('id')  # 가나다순으로 정렬
        elif sort== 'views':
            mountains = mountains.order_by('-views')  # 조회순으로 정렬
        elif sort == 'height':
            mountains = mountains.order_by('height') # 고도순으로 정렬

    page= request.GET.get('page', '1')
    per_page = 12
    paginator = Paginator(mountains, per_page)
    page_obj = paginator.get_page(page)        
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mountains/mountain_list.html', context)


class CourseListView(ListView):
    template_name = 'mountains/course_list.html'
    context_object_name = 'courses'
    model = Course
    paginate_by = 5    

    def get_queryset(self):
        mountain_pk = self.kwargs['mountain_pk']
        mountain = Mountain.objects.get(pk=mountain_pk)
        sort = self.request.GET.get('sort', '')  # 정렬 옵션 가져오기

        queryset = Course.objects.filter(mntn_name=mountain)

        if sort== 'bookmarks':
            queryset = queryset.annotate(num_bookmarks=Count('bookmarks')).order_by('-num_bookmarks')
        elif sort == 'distance':
            queryset = queryset.order_by('distance')
        elif sort == 'hidden_time':
            queryset = queryset.order_by('hidden_time')
        elif sort == 'diff':
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
        mountain = Mountain.objects.get(pk=mountain_pk)
        queryset = self.get_queryset()  # get_queryset 메서드 호출
            
        # 페이지네이션
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        serializer = Serializer()
        data = {}
        for course in page_obj:
            geojson_data = serializer.serialize([course], geometry_field='geom')
            data[course.pk] = geojson_data

        context.update({
            'mountain': mountain,
            'courses': page_obj,
            'courses_data': data,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
        })
        return context     


def course_all_list(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        sido = request.POST.get('sido1', '')  # 선택한 시/도 값 가져오기
        gugun = request.POST.get('gugun1', '')

        if sido and gugun:
            if ('광역시' in sido) or ('특별시' in sido):
                mountain = Mountain.objects.filter(Q(region__contains=sido))
                courses = courses.filter(mntn_name__in=mountain)
            else:
                if '전체' in gugun:
                    mountain = Mountain.objects.filter(Q(region__contains=sido))
                    courses = courses.filter(mntn_name__in=mountain)
                else:
                    mountain = Mountain.objects.filter(Q(region__contains=sido) & Q(region__contains=gugun))
                    courses = courses.filter(mntn_name__in=mountain)
        # 필터링된 객체를 세션에 저장
        request.session['filtered_courses'] = list(courses.values_list('pk', flat=True))

    elif request.method == 'GET':
        filtered_pks = request.session.get('filtered_courses', [])
        if filtered_pks:
            courses = Course.objects.filter(pk__in=filtered_pks)
        else:
            courses = Course.objects.all()

        sort = request.GET.get('sort', None)

        if sort == 'bookmarks':
            courses = courses.annotate(bookmarks_count=Count('bookmarks')).order_by('-bookmarks_count')

        elif sort == 'hidden_time':
            courses = courses.order_by('hidden_time')

        elif sort == 'distance':
            courses = courses.order_by('distance')            
        
        elif sort == 'id':
            courses = courses.order_by('id') 

        elif sort == 'diff':
            courses = courses.annotate(
                diff_order=Case(
                    When(diff='하', then=1),
                    When(diff='중', then=2),
                    When(diff='상', then=3),
                    default=4
                )
            ).order_by('diff_order')    

    page= request.GET.get('page', '1')
    per_page = 10
    paginator = Paginator(courses, per_page)
    page_obj = paginator.get_page(page)        
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mountains/course_all_list.html', context)


def mountain_likes(request, mountain_pk):
    mountain = get_object_or_404(Mountain, pk=mountain_pk)
    user = request.user
    if user in mountain.likes.all():
        mountain.likes.remove(user)
        is_liked = False
    else:
        mountain.likes.add(user)
        is_liked = True

    return JsonResponse({'is_liked': is_liked, 'like_count':mountain.likes.count()})    


def bookmark(request, mountain_pk, course_pk):
    course = Course.objects.get(pk=course_pk)
    user = request.user
    is_bookmarked = user.bookmarks.filter(pk=course_pk).exists()
    if is_bookmarked:
        user.bookmarks.remove(course)
        is_bookmarked = False
    else:
        user.bookmarks.add(course)
        is_bookmarked = True
    context = {
        'is_bookmarked' : is_bookmarked,
    }
    return JsonResponse(context)



class CourseDetailView(DetailView):
    model = Course
    template_name = 'mountains/course_detail.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        # mountain_pk = self.kwargs['mountain_pk']
        course_pk = self.kwargs['pk']
        # mountain = get_object_or_404(Mountain, pk=mountain_pk)
        course = get_object_or_404(Course, pk=course_pk)
        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        mountain = course.mntn_name

        serializer = Serializer()
        data = {course.pk: serializer.serialize([course], geometry_field='geom')}

        context.update({
            'mountain': mountain,
            'course': course,
            'course_data': data
        })
        return context