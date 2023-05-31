from django.urls import path
from .views import *

app_name = 'mountains'
urlpatterns = [
    path('mountain_list/', MountainListView.as_view(), name='mountain_list'),
    path('<int:pk>/', MountainDetailView.as_view(), name='mountain_detail'),
    path('<int:mountain_pk>/courses/', CourseListView.as_view(), name='course_detail'),

]