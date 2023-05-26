from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:user_pk>/', views.profile, name='profile'),
    path('profile/<int:user_pk>/delete', views.delete, name='delete'),
]