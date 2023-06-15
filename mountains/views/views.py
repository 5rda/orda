import gpxpy, gpxpy.gpx, os, datetime
from mountains.models import *
from mountains.forms import SearchForm
from utils.weather import get_weather
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.db.models import Count, When, Case, Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.views.generic import ListView, FormView, View
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.gis.serializers.geojson import Serializer

class SearchView(FormView):
    template_name = 'mountains/search.html'
    form_class = SearchForm
    success_url = 'mountains/mountain_list.html'


def mountain_list(request):
    mountains = Mountain.objects.all()
    if request.method == 'POST':
        tags = request.POST.getlist('tags')
        sido = request.POST.get('sido2')
        gugun = request.POST.get('gugun2')
        search_query = request.POST.get('search_query')
        filter_condition = Q()

        if sido and gugun:
            if ('광역시' in sido) or ('특별시' in sido):
                filter_condition.add(Q(region__contains=sido), filter_condition.AND)
            else:
                if '전체' in gugun:
                    filter_condition.add(Q(region__contains=sido), filter_condition.AND)
                else:
                    filter_condition.add(Q(region__contains=sido) & Q(region__contains=gugun), filter_condition.AND)

        if tags:
            filtered_mountains = mountains.filter(review__tags__pk__in=tags).distinct()
            int_tags = list(map(int, tags))
            filtered_pks = []
            for filtered_mountain in filtered_mountains:
                # print(f'산:{filtered_mountain.top_tags_pk}')
                # print(f'태그:{int_tags}')
                top_tags_pk = filtered_mountain.top_tags_pk
                if any((tag_pk in top_tags_pk) for tag_pk in int_tags):
                    filtered_pks.append(filtered_mountain.pk)
            mountains = mountains.filter(pk__in=filtered_pks)

        if search_query:
            mountains = mountains.filter(name__icontains=search_query)

        mountains = mountains.filter(filter_condition)

        # 필터링된 객체를 세션에 저장
        request.session['filtered_mountains'] = list(mountains.values_list('pk', flat=True))            

    elif request.method == 'GET':
        # GET 요청 처리
        filtered_pks = request.session.get('filtered_mountains', [])
        if filtered_pks:
            mountains = Mountain.objects.filter(pk__in=filtered_pks)
        else:
            mountains = Mountain.objects.all()
        sort = request.GET.get('sort', None)
            
        if sort== 'likes':
            mountains = mountains.annotate(likes_count=Count('likes')).order_by('-likes_count')  # 좋아요순으로 정렬
        elif sort == 'reviews':
            mountains = mountains.annotate(reviews_count2=Count('review')).order_by('-reviews_count2') # 리뷰순으로 정렬
        elif sort == 'id':
            mountains = mountains.order_by('id')  # 가나다순으로 정렬
        elif sort== 'views':
            mountains = mountains.order_by('-views')  # 조회순으로 정렬
        elif sort == 'height':
            mountains = mountains.order_by('height') # 고도순으로 정렬

    page= request.GET.get('page', '1')
    per_page = 12
    paginator = Paginator(mountains, per_page)
    page_obj = paginator.get_page(page)        
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mountains/mountain_list.html', context)


class CourseListView(LoginRequiredMixin, ListView):
    template_name = 'mountains/course_list.html'
    context_object_name = 'courses'
    model = Course
    paginate_by = 5    

    def get_queryset(self):
        mountain_pk = self.kwargs['mountain_pk']
        mountain = Mountain.objects.get(pk=mountain_pk)
        sort = self.request.GET.get('sort', '')  # 정렬 옵션 가져오기

        queryset = Course.objects.filter(mntn_name=mountain)

        if sort== 'bookmarks':
            queryset = queryset.annotate(num_bookmarks=Count('bookmarks')).order_by('-num_bookmarks')
        elif sort == 'distance':
            queryset = queryset.order_by('distance')
        elif sort == 'hidden_time':
            queryset = queryset.order_by('hidden_time')
        elif sort == 'diff':
            # 난이도 정렬을 추가
            queryset = queryset.annotate(
                diff_order=Case(
                    When(diff='하', then=1),
                    When(diff='중', then=2),
                    When(diff='상', then=3),
                    default=4
                )
            ).order_by('diff_order')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mountain_pk = self.kwargs['mountain_pk']
        mountain = Mountain.objects.get(pk=mountain_pk)
        queryset = self.get_queryset()  # get_queryset 메서드 호출
            
        # 페이지네이션
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        serializer = Serializer()
        detail_serializer = Serializer()
        data = {}
        detail_data = {}
        for course in page_obj:
            detail = CourseDetail.objects.filter(crs_name_detail=course)
            geojson_detail_data = detail_serializer.serialize(detail, fields=('geom', 'waypoint_name', 'waypoint_category'))
            geojson_data = serializer.serialize([course], geometry_field='geom')
            data[course.pk] = geojson_data
            detail_data[course.pk] = geojson_detail_data

        context.update({
            'mountain': mountain,
            'courses': page_obj,
            'courses_data': data,
            'detail_data': detail_data,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
        })
        return context     


def course_all_list(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        sido = request.POST.get('sido1', '')  # 선택한 시/도 값 가져오기
        gugun = request.POST.get('gugun1', '')

        if sido and gugun:
            if ('광역시' in sido) or ('특별시' in sido):
                mountain = Mountain.objects.filter(Q(region__contains=sido))
                courses = courses.filter(mntn_name__in=mountain)
            else:
                if '전체' in gugun:
                    mountain = Mountain.objects.filter(Q(region__contains=sido))
                    courses = courses.filter(mntn_name__in=mountain)
                else:
                    mountain = Mountain.objects.filter(Q(region__contains=sido) & Q(region__contains=gugun))
                    courses = courses.filter(mntn_name__in=mountain)
        # 필터링된 객체를 세션에 저장
        request.session['filtered_courses'] = list(courses.values_list('pk', flat=True))

    elif request.method == 'GET':
        filtered_pks = request.session.get('filtered_courses', [])
        if filtered_pks:
            courses = Course.objects.filter(pk__in=filtered_pks)
        else:
            courses = Course.objects.all()

        sort = request.GET.get('sort', None)

        if sort == 'bookmarks':
            courses = courses.annotate(bookmarks_count=Count('bookmarks')).order_by('-bookmarks_count')

        elif sort == 'hidden_time':
            courses = courses.order_by('hidden_time')

        elif sort == 'distance':
            courses = courses.order_by('distance')            
        
        elif sort == 'id':
            courses = courses.order_by('id') 

        elif sort == 'diff':
            courses = courses.annotate(
                diff_order=Case(
                    When(diff='하', then=1),
                    When(diff='중', then=2),
                    When(diff='상', then=3),
                    default=4
                )
            ).order_by('diff_order')    

    page= request.GET.get('page', '1')
    per_page = 10
    paginator = Paginator(courses, per_page)
    page_obj = paginator.get_page(page)        
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mountains/course_all_list.html', context)


def reset_filter(request):
    if 'filtered_courses' in request.session:
        # 세션에서 'filtered_courses' 키 제거
        request.session.pop('filtered_courses')
        # 세션을 수정한 것을 알림
        request.session.modified = True  
        return redirect('mountains:course_all_list')
    
    elif 'filtered_mountains' in request.session:
        request.session.pop('filtered_mountains')
        request.session.modified = True  
        return redirect('mountains:mountain_list')
    
    else:
        return HttpResponseBadRequest("Bad Request")


@login_required
def mountain_likes(request, mountain_pk):
    mountain = get_object_or_404(Mountain, pk=mountain_pk)
    user = request.user
    if user in mountain.likes.all():
        mountain.likes.remove(user)
        is_liked = False
    else:
        mountain.likes.add(user)
        is_liked = True

    return JsonResponse({'is_liked': is_liked, 'like_count':mountain.likes.count()})    


@login_required
def bookmark(request, mountain_pk, course_pk):
    course = Course.objects.get(pk=course_pk)
    user = request.user
    is_bookmarked = user.bookmarks.filter(pk=course_pk).exists()
    if is_bookmarked:
        user.bookmarks.remove(course)
        is_bookmarked = False
    else:
        user.bookmarks.add(course)
        is_bookmarked = True
    context = {
        'is_bookmarked' : is_bookmarked,
    }
    return JsonResponse(context)


class gpxDownloadView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)    
    
    def post(self, request, mountain_pk, course_pk):
        course = Course.objects.get(pk=course_pk)
        geom = course.geom
        name = course.crs_name_detail

        # GPX 파일 생성 및 변환
        gpx_data = self.create_gpx(geom, name)

        # 이메일 전송
        email = request.user.email  # 유저의 이메일 주소를 가져옵니다.
        if email:
            self.send_email(email, gpx_data, name)  # 이메일로 GPX 파일을 전송합니다.
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    def create_gpx(self, geom, name):
        # 등산 코스의 geom 데이터를 GPX 형식으로 변환하는 로직을 구현합니다.
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        # LineString의 좌표들을 가져와서 GPX 세그먼트에 추가합니다.
        for point in geom.coords:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=point[1], longitude=point[0]))

        # GPX 데이터를 반환합니다.
        gpx_data = gpx.to_xml()
        return gpx_data    

    def send_email(self, email, gpx_data, name):
        # 이메일을 전송하는 로직을 구현합니다.
        email_subject = f'[오르다] {name} 등산 코스 GPX 파일'
        email_body = render_to_string('mountains/email.html', {'name': name})
        email_attachment = (f"{name.replace(' ', '_')}_course.gpx", gpx_data, "application/gpx+xml")

        email_message = EmailMessage(email_subject, email_body, os.getenv('DEFAULT_FROM_EMAIL'), [email])
        email_message.attach(*email_attachment)
        email_message.send()
        

@login_required        
def weather_forecast(request, pk):
    mountain = Mountain.objects.get(pk=pk)
    lat = mountain.geom.y
    lon = mountain.geom.x
    api_key = os.environ['OPEN_WEATHER_KEY']

    weather_data = get_weather(lat, lon, api_key)

    daily_data = {}  # 날짜별 데이터를 담을 딕셔너리

    def get_direction(deg):
        if 22.5 <= deg < 67.5:
            return '북동'
        elif 67.5 <= deg < 112.5:
            return '동'
        elif 112.5 <= deg < 157.5:
            return '남동'
        elif 157.5 <= deg < 202.5:
            return '남'
        elif 202.5 <= deg < 247.5:
            return '남서'
        elif 247.5 <= deg < 292.5:
            return '서'
        elif 292.5 <= deg < 337.5:
            return '북서'
        else:
            return '북'

    for forecast in weather_data['list']:
        dt_txt = datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)
        date_key = dt_txt.strftime('%d일')  # 날짜를 key로 사용
        forecast['dt_txt'] = dt_txt.strftime('%H시')
        forecast['pop'] = int(forecast['pop'] * 100)
        forecast['wind']['deg'] = get_direction(forecast['wind']['deg'])

        if date_key not in daily_data:
            daily_data[date_key] = []  # 새로운 날짜의 데이터를 빈 리스트로 초기화

        daily_data[date_key].append(forecast)  # 해당 날짜에 데이터 추가

    context = {
        'mountain': mountain,
        'weather_data': weather_data,
        'daily_data': daily_data,
    }

    return render(request, 'mountains/weather_forecast.html', context)


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'mountains/course_detail.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        # mountain_pk = self.kwargs['mountain_pk']
        course_pk = self.kwargs['pk']
        # mountain = get_object_or_404(Mountain, pk=mountain_pk)
        course = get_object_or_404(Course, pk=course_pk)
        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        mountain = course.mntn_name
        detail = CourseDetail.objects.filter(crs_name_detail=course)

        serializer = Serializer()
        detail_serializer = Serializer()

        data = {course.pk: serializer.serialize([course], geometry_field='geom')}
        detail_data = {course.pk: detail_serializer.serialize(detail, fields=('geom', 'waypoint_name', 'waypoint_category'))}

        context.update({
            'mountain': mountain,
            'course': course,
            'course_data': data,
            'detail_data': detail_data,
        })
        return context