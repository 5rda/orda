from django.urls import path
from .views import *

app_name = 'mountains'
urlpatterns = [
    path('', MountainListView.as_view(), name='mountain_list'),
    path('<int:pk>/', MountainDetailView.as_view(), name='mountain_detail'),
    path('<int:mountain_pk>/course/<int:course_pk>/bookmark/', bookmark, name='bookmark')
]