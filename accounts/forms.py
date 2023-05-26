from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="아이디")
    nickname = forms.CharField(label="닉네임")
    email = forms.EmailField(label="이메일", required=False)
    profile = forms.ImageField(label="프로필 이미지", required=False)
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "nickname", "email", "profile")