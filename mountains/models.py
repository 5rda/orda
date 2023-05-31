# from django.db import models
from django.contrib.gis.db import models
from django.db.models import Sum
from django.contrib.gis.db.models.functions import Length, Transform

# Create your models here.
class Mountain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50 , unique=True)
    subname = models.CharField(max_length=200)
    height = models.FloatField()
    region = models.CharField(max_length=100)
    diff = models.CharField(max_length=30)
    geom = models.GeometryField()

    class Meta:
        managed = False
        db_table = 'mountains'

    def __str__(self):
        return self.name
        
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    mntn_name = models.ForeignKey(Mountain, on_delete=models.CASCADE, to_field="name", db_column="mntn_name")
    crs_name = models.CharField(max_length=100, unique=True)
    distance = models.IntegerField(db_column='total_distance_int')
    duration = models.DurationField(db_column='total_duration_int')

    class Meta:
        managed = False
        db_table = 'course'

    def __str__(self):
        return self.crs_name


class CourseDetail(models.Model):
    id = models.AutoField(primary_key=True)
    crs_name = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="crs_name", db_column="crs_name")
    is_waypoint = models.BooleanField(default=False)
    waypoint_name = models.CharField(max_length=50)
    geom = models.GeometryField()

    class Meta:
        managed = False
        db_table = 'course_detail'

    def __str__(self):
        return str(self.crs_name)
    

class Comment(models.Model):
    pass