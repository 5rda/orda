from django.urls import path
from .views import *

app_name = 'mountains'
urlpatterns = [
    path('', MountainListView.as_view(), name='mountain_list'),
    path('<int:pk>/', MountainDetailView.as_view(), name='mountain_detail'),
    path('<int:mountain_pk>/likes/', mountain_likes, name='mountain_likes'),
    path('<int:mountain_pk>/course/<int:course_pk>/bookmark/', bookmark, name='bookmark'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/create_review/', create_review, name='create_review'),
    path('<int:pk>/review_likes/<int:review_pk>/', review_likes, name='review_likes'),
    path('<int:pk>/review_delete/<int:review_pk>/', review_delete, name='review_delete'),

]

