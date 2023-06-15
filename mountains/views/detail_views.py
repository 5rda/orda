import json, urllib.request, requests, datetime, math, os
from mountains.models import *
from mountains.forms import ReviewCreationForm
from datetime import date, datetime, timedelta
from urllib.parse import urlencode, quote_plus, unquote
from django.db.models import F
from django.views.generic import DetailView
from django.contrib.gis.serializers.geojson import Serializer
from django.contrib.auth.mixins import LoginRequiredMixin

class MountainDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mountains/mountain_detail.html'
    context_object_name = 'mountain'
    model = Mountain

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.session.get('mountain_viewed_{}'.format(self.object.pk), False):
            Mountain.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
            request.session['mountain_viewed_{}'.format(self.object.pk)] = True

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 산관련
        mountain = self.get_object()
        serializer = Serializer()
        courses = mountain.course_set.all()
        data = {}
        for course in courses:
            geojson_data = serializer.serialize([course], geometry_field='geom')
            data[course.pk] = geojson_data

        # 리뷰 관련
        reviews = Review.objects.filter(mountain=mountain).order_by('-created_at')
        most_liked_review = reviews.annotate(num_likes=Count('like_users')).order_by('-num_likes').first()

        context = {
            # 산 관련
            'mountain': mountain,
            'courses': courses,
            'courses_data': data,

            # 리뷰 관련
            'form': ReviewCreationForm(),
            'reviews': reviews,
            'most_liked_review': most_liked_review,
        }
        
        return context
