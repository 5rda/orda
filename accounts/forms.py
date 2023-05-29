from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(
            attrs={
                'class': 'appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '아이디를 입력하세요',
                'id': "아이디",
            }
        )
    )
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '비밀번호를 입력하세요',
                'id': "비밀번호",
            }
        )
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '비밀번호를 확인하세요',
                'id': "비밀번호 확인",
            }
        )
    )
    nickname = forms.CharField(
        label="닉네임",
        widget=forms.TextInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '닉네임를 입력하세요',
                'id': "닉네임",
            }
        )
    )

    email = forms.EmailField(
        label="이메일", 
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': '"appearance-none bg-transparent border-none text-gray-700  py-1 px-2 leading-tight focus:outline-none',
                'style': 'width: 96%',
                'placeholder': '이메일을 입력하세요',
                'id': "이메일",
            }
        ))
    profile = forms.ImageField(
        label="프로필 이미지", 
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class" : "d-none ",
                'id': "프로필 이미지",
            }
        )
        )
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "nickname", "email", "profile")




class CustomUserChangeForm(UserChangeForm):
    nickname = forms.CharField(label="닉네임")
    email = forms.EmailField(label="이메일", required=False)
    profile = forms.ImageField(label="프로필 이미지", required=False)
    message = forms.CharField(label="상태메시지", required=False)
    class Meta:
        model = get_user_model()
        fields = ("nickname", "email", "profile", "message")