from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.files import File
from urllib.request import urlopen
import requests
import os
from dotenv import load_dotenv


def login(request):
    if request.user.is_authenticated:
        return redirect('mountains:index', request.user.pk)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('mountains:index', request.user.pk )
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('mountains:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('mountains:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('mountains:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def profile(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('mountains:index')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('mountains:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_change.html', context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    if request.user != person:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
        else:
            person.followers.add(request.user)
    return redirect('accounts:profile', person.pk)


load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID')


def kakao_login(request):
    client_id = CLIENT_ID
    redirect_uri = 'http://localhost:8000/accounts/kakao/callback/'
    url = f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    return redirect(url)


def kakao_callback(request):
    User = get_user_model()
    code = request.GET.get('code')
    if code:
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'redirect_uri': 'http://localhost:8000/accounts/kakao/callback/',
            'code': code,
        }
        response = requests.post(url, data=data)
        token = response.json().get('access_token')
        if token:
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
            user_info = response.json()

            kakao_user_id = user_info['id']
            nickname = user_info['properties']['nickname']
            email = user_info['kakao_account']['email']
            profile_img = user_info['properties']['profile_image']

            user, created = User.objects.get_or_create(kakao_user_id=kakao_user_id)

            if created:
                user.nickname = nickname
                user.email = email
                if 'http://' in profile_img:
                    profile_img = profile_img.replace('http://', '')
                else:
                    profile_img = profile_img

                image_url = f"http://{profile_img}"
                response = urlopen(image_url)
                user.profile_img.save(f"{kakao_user_id}.png", File(response))
            auth_login(request, user)
            return redirect('mountains:index')
    return redirect('accounts:login')
