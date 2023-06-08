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
from django.http import JsonResponse
from bs4 import BeautifulSoup
from mountains.models import Mountain, Course, CourseDetail
from .models import VisitedCourse
from django.contrib.gis.serializers.geojson import Serializer


def login(request):
    if request.user.is_authenticated:
        return render(request, 'pjt/index.html')
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            prev_url = request.session.get('prev_url')
            if prev_url:
                del request.session['prev_url']
                return redirect(prev_url)
            return render(request, 'pjt/index.html')
    else:
        form = CustomUserAuthenticationForm()
    request.session['prev_url'] = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'pjt/index.html')


def signup(request):
    if request.user.is_authenticated:
        return render(request, 'pjt/index.html')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return render(request, 'pjt/index.html')
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
    reviews = person.review_set.all().count()
    posts_comments = person.postcomment_set.all().count()
    visited_courses = person.visitedcourse_set.all().count()

    liked_posts = Post.objects.filter(like_users=person)
    liked_mountains = Mountain.objects.filter(likes=person)
    bookmark_course = Course.objects.filter(bookmarks=person)

    serializer = Serializer()
    course_details = {}
    for course in bookmark_course:
        geojson_data = serializer.serialize(CourseDetail.objects.filter(crs_name_detail=course), fields=('geom', 'is_waypoint', 'waypoint_name', 'crs_name_detail'))
        course_details[course.pk] =geojson_data
    
    score = posts.count() * 40 + reviews * 30 + visited_courses * 20 + posts_comments * 5

    if score < 200:
        level = 1
        rest = score
        max_score = 200
    elif score < 300:
        level = 2
        rest = score-200
        max_score = 300
    elif score < 400:
        level = 3
        rest = score-300
        max_score = 400
    elif score < 500:
        level = 4
        rest = score-400
        max_score = 500
    else:
        level = 5
        rest = score-500
        if rest < 600:
            rest = score-500
        else:
            rest = 600
        max_score = 600

    # 추가
    expbar = (score / max_score) * 100
    restexp = max_score - score

    level_dict = {1:'등산새싹', 2:'등산샛별', 3:'등산인', 4:'등산고수', 5:'등산왕'}
    context = {
        'person': person,
        'post': post,
        'posts': posts,
        'level': level,
        'level_name': level_dict[level],
        'rest': rest,
        'max_score': max_score,
        'liked_posts': liked_posts,
        'liked_mountains': liked_mountains,
        'bookmark_course': bookmark_course,
        'course_details': course_details,

        # 추가
        'score': score,
        'expbar': expbar,
        'restexp': restexp,
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
    return render(request, 'pjt/index.html')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomUserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile', request.user.pk)
    else:
        form = CustomUserPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_change.html', context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    person  = User.objects.get(pk=user_pk)
    me = request.user

    if person != me:
        if me in person.followers.all():
            person.followers.remove(me)
            is_followed = False
        else:
            person.followers.add(me)
            is_followed = True
        context = {
            'is_followed':is_followed,
            'followings_count':person.followings.count(),
            'followers_count':person.followers.count(),
            'followers': [{'username': f.username,'pk': f.pk} for f in person.followers.all()]
        }
        return JsonResponse(context)
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
            email = user_info['kakao_account']['email']
            profile_img = user_info['properties']['profile_image']

            user, created = User.objects.get_or_create(kakao_user_id=kakao_user_id)

            if created:
                user.username = kakao_user_id
                user.email = email
                if 'http://' in profile_img:
                    profile_img = profile_img.replace('http://', '')
                else:
                    profile_img = profile_img

                image_url = f"http://{profile_img}"
                response = urlopen(image_url)
                user.profile_img.save(f"{kakao_user_id}.png", File(response))
                auth_login(request, user)
                return redirect('accounts:update')
            else:
                auth_login(request, user)
                return render(request, 'pjt/index.html')
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

            naver_user_id = user_info['response']['id']
            if 'email' in user_info['response']:
                email = user_info['response']['email']
            else:
                email = None
            if 'profile_image' in user_info['response']:
                profile_img = user_info['response']['profile_image']
            else:
                profile_img = None

            user, created = User.objects.get_or_create(naver_user_id=naver_user_id)

            if created:
                user.username = naver_user_id
                user.email = email
                response = urlopen(profile_img)
                user.profile_img.save(f"{naver_user_id}.png", File(response))
                auth_login(request, user)
                return redirect('accounts:update')
            else:
                auth_login(request, user)
                return render(request, 'pjt/index.html')
    return redirect('accounts:login')


def get_first_image_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    print(img_tag)
    if img_tag:
        return img_tag['src']
    else:
        return None
    

@login_required
def my_memories(request):
    mountains = Mountain.objects.all()
    visited_courses = request.user.visited_courses.all()
    visited_mountains = (
        VisitedCourse.objects.filter(user=request.user)
        .values_list('mountain_name', flat=True)
        .distinct()
    )

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)

        if course in visited_courses:
            request.user.visited_courses.remove(course)
        else:
            VisitedCourse.objects.create(
                user=request.user,
                course=course,
                mountain_name=course.mntn_name,
                mountain_id=course.mntn_name.id
            )
        return redirect('accounts:my_memories')

    context = {
        'mountains': mountains,
        'visited_courses': visited_courses,
        'visited_mountains': visited_mountains,
    }
    return render(request, 'accounts/my_memories.html', context)





