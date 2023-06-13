from django.urls import path
from .views import *

app_name = 'mountains'
urlpatterns = [
    path('', mountain_list, name='mountain_list'),
    path('<int:pk>/', MountainDetailView.as_view(), name='mountain_detail'),
    path('<int:mountain_pk>/likes/', mountain_likes, name='mountain_likes'),
    path('<int:mountain_pk>/courses/', CourseListView.as_view(), name='course_list'),
    path('<int:mountain_pk>/course/<int:course_pk>/bookmark/', bookmark, name='bookmark'),
    path('<int:mountain_pk>/courses/<int:course_pk>/download/', gpxDownloadView.as_view(), name='download'),
    path('courses/', course_all_list, name='course_all_list'),
    path('<int:pk>/create_review/', create_review, name='create_review'),
    path('<int:pk>/review_likes/<int:review_pk>/', review_likes, name='review_likes'),
    path('<int:pk>/review_delete/<int:review_pk>/', review_delete, name='review_delete'),
    path('<int:pk>/review_update/<int:review_pk>/', review_update, name='review_update'),
    path('<int:pk>/review_image_delete/<int:review_pk>/', review_image_delete, name='review_image_delete'),
    path('search/', SearchView.as_view(), name='search'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('weather_forecast/<int:pk>/', weather_forecast, name='weather_forecast'),
    path('reset/', reset_filter, name='reset'),
]
