# from django.db import models
from django.contrib.gis.db import models
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your models here.
class Mountain(models.Model):

    def image_path(instance, filename):
        return f'mountains/{instance.name}/{filename}'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50 , unique=True)
    subname = models.CharField(max_length=200)
    height = models.IntegerField()
    region = models.CharField(max_length=100)
    diff = models.CharField(max_length=30)
    geom = models.GeometryField()
    image = models.ImageField(upload_to=image_path, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_mountains', db_table='mountains_mountain_likes')
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        managed = False
        db_table = 'mountains_mountain'
        ordering = ['id']

    @property
    def reviews_count(self):
        return self.review_set.count()    

    def __str__(self):
        return self.name
        

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    mntn_name = models.ForeignKey(Mountain, on_delete=models.CASCADE, to_field="name", db_column="mntn_name")
    crs_name = models.CharField(max_length=100, unique=True)
    distance = models.IntegerField(db_column='total_distance_int')
    duration = models.DurationField(db_column='total_duration_int')
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL,  related_name='bookmarks',  db_table='mountains_course_bookmarks')

    class Meta:
        managed = False
        db_table = 'mountains_course'
        ordering = ['id']

    def __str__(self):
        return self.crs_name
    

class CourseDetail(models.Model):
    id = models.AutoField(primary_key=True)
    crs_name = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="crs_name", db_column="crs_name")
    is_waypoint = models.BooleanField(default=False)
    waypoint_name = models.CharField(max_length=50)
    waypoint_category = models.CharField(max_length=256, db_column='category')
    geom = models.GeometryField()

    class Meta:
        managed = False
        db_table = 'mountains_coursedetail'
        ordering = ['id']

    def __str__(self):
        return str(self.crs_name)


class Review(models.Model):
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200)

    def __str__(self):
        return self.content


# class CourseBookmark(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'mountains_course_bookmarks'

