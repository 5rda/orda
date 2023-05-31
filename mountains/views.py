from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import *
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
        context['courses'] = mountain.course_set.order_by('crs_name')
        return context
    

class CourseListView(ListView):
    template_name = 'mountains/course_list.html'
    context_object_name = 'courses'
    model = Course

    def get_queryset(self):
        mountain_pk = self.kwargs['mountain_pk']
        return super().get_queryset().filter(mntn_name__id=mountain_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = context['courses']
        course_details_list = []
        if isinstance(courses, Course):
            # courses가 단일 Course 객체인 경우
            course_details = CourseDetail.objects.filter(crs_name=courses)
            course_details_list.extend(course_details)
        else:
            # courses가 QuerySet인 경우
            for course in courses:
                course_details = CourseDetail.objects.filter(crs_name=course)
                course_details_list.extend(course_details)
        context['course_details'] = course_details_list
        return context

