from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.contrib.gis.serializers.geojson import Serializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
import json, os
from django.conf import settings
# Create your views here.

def index(request):
    return render(request, 'mountains/index.html')


class MountainListView(ListView):
    template_name = 'mountains/mountain_list.html'
    context_object_name = 'mountains'
    model = Mountain

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mountain = self.get_object()
        serializer = Serializer()
        courses = mountain.course_set.all()
        course_details = {}
        for course in courses:
            geojson_data = serializer.serialize(CourseDetail.objects.filter(crs_name=course), fields=('geom', 'is_waypoint', 'waypoint_name'))
            course_details[course.pk] =geojson_data
        context = {
            'mountain': mountain,
            'courses': courses,
            'course_details': course_details
        }
        # json_data = json.dumps(course_details, indent=4, sort_keys=True, ensure_ascii=False)
        # file_path = os.path.join(settings.STATICFILES_DIRS[0], 'course_details.json')
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     file.write(json_data)
        return context

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
    
    return JsonResponse({'is_bookmarked': is_bookmarked})