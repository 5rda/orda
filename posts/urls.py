from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/likes/', views.likes, name='likes'),
    path('<int:post_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_likes/', views.comment_likes, name='comment_likes'),
    path('<int:post_pk>/comments/<int:comment_pk>/comment_dislikes/', views.comment_dislikes, name='comment_dislikes'),
    path('search/', views.search, name='search'), 
    path('proofshot/', views.proofshot, name='proofshot'), 
]