from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserAuthenticationForm, CustomUserPasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from urllib.request import urlopen
from posts.models import Post
import requests
import os
from dotenv import load_dotenv


def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile', request.user.pk)
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # return redirect('mountains:index', request.user.pk )
            return redirect('accounts:profile', request.user.pk )

    else:
        form = CustomUserAuthenticationForm()
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
            return redirect('accounts:profile', request.user.pk )
            # return redirect('mountains:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def profile(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    post = Post.objects.filter(user=person)
    posts = person.post_set.all().order_by('-created_at')
    liked_posts = Post.objects.filter(like_users=request.user)
    posts_comments = person.postcomment_set.all().count()
    # mountains_comments = person.comment_set.all().count()
    # score = posts.count() * 40 + mountains_comments * 30 + posts_comments * 5

    # if score < 200:
    #     level = 1
    #     rest = score
    #     max_score = 200
    # elif score < 300:
    #     level = 2
    #     rest = score-200
    #     max_score = 300
    # elif score < 400:
    #     level = 3
    #     rest = score-300
    #     max_score = 400
    # elif score < 500:
    #     level = 4
    #     rest = score-400
    #     max_score = 500
    # else:
    #     level = 5
    #     rest = score-500
    #     if rest < 600:
    #         rest = score-500
    #     else:
    #         rest = 600
    #     max_score = 600

    # level_dict = {1:'등산새싹', 2:'등산샛별', 3:'등산인', 4:'등산고수', 5:'등산왕'}
    context = {
        'person': person,
        'post': post,
        'posts': posts,
        # 'level': level,
        # 'level_name': level_dict[level],
        # 'rest': rest,
        # 'max_score': max_score,
        'liked_posts': liked_posts,
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
        form = CustomUserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('mountains:index')
    else:
        form = CustomUserPasswordChangeForm(request.user)
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
KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID')
NAVER_CLIENT_ID = os.environ.get('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.environ.get('NAVER_CLIENT_SECRET')


def kakao_login(request):
    client_id = KAKAO_CLIENT_ID
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
            'client_id': KAKAO_CLIENT_ID,
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


def naver_login(request):
    client_id = NAVER_CLIENT_ID
    redirect_uri = 'http://localhost:8000/accounts/naver/callback/'
    url = f'https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state=STATE_STRING'
    return redirect(url)


def naver_callback(request):
    User = get_user_model()
    code = request.GET.get('code')
    if code:
        url = 'https://nid.naver.com/oauth2.0/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': NAVER_CLIENT_ID,
            'client_secret': NAVER_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8000/accounts/naver/callback/',
            'code': code,
        }
        response = requests.post(url, data=data)
        token = response.json().get('access_token')
        if token:
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
            user_info = response.json()
            print(user_info)

            naver_user_id = user_info['response']['id']
            nickname = user_info['response']['nickname']
            email = user_info['response']['email']
            profile_img = user_info['response']['profile_image']

            user, created = User.objects.get_or_create(naver_user_id=naver_user_id)

            if created:
                user.nickname = nickname
                user.email = email
                response = urlopen(profile_img)
                user.profile_img.save(f"{naver_user_id}.png", File(response))
            auth_login(request, user)
            return redirect('accounts:profile', user.pk)
    return redirect('accounts:login')