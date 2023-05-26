from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:user_pk>/', views.profile, name='profile'),
    path('profile/update/', views.update, name='update'),
    path('profile/delete/', views.delete, name='delete'),
    path('profile/password_change/', views.password_change, name='password_change'),
]