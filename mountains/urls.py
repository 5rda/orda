from django.urls import path
from .views import *
from . import views

app_name = 'mountains'
urlpatterns = [
    path('', MountainListView.as_view(), name='mountain_list'),
    path('<int:pk>/', MountainDetailView.as_view(), name='mountain_detail'),
    path('<int:pk>/create_review/', views.create_review, name='create_review'),

]