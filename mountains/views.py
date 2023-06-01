from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.contrib.gis.serializers.geojson import Serializer
from django.shortcuts import get_object_or_404
from .models import *
import json, os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.

def index(request):
    return render(request, 'mountains/index.html')


class MountainListView(ListView):
    template_name = 'mountains/mountain_list.html'
    context_object_name = 'mountains'
    model = Mountain


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
        # print(course_details)
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
