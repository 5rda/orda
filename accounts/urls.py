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
    path('profile/password/', views.password_change, name='password_change'),
    path('profile/<int:user_pk>/follow', views.follow, name='follow'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('naver/login/', views.naver_login, name='naver_login'),
    path('naver/callback/', views.naver_callback, name='naver_callback'),
]