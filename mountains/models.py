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
    crs_name = models.CharField(max_length=30)
    is_waypoint = models.BooleanField(default=False)
    waypoint_name = models.CharField(max_length=50)
    geom = models.GeometryField()

    class Meta:
        managed = False
        db_table = 'test_course'

    def __str__(self):
        return self.crs_name
    
    # @property
    # def total_distance(self):
    #     total_distance = Course.objects.filter(crs_name=self.crs_name).annotate(distance=Length(Transform('geom', 3857))).aggregate(distance=Sum('distance'))['distance']
    #     return total_distance

    # @property
    # def total_duration(self):
    #     distance = self.total_distance
    #     speed = 1.4  # m/s
    #     total_seconds = distance / speed if distance else None
    #     hours = int(total_seconds // 3600)
    #     minutes = int((total_seconds % 3600) // 60)
    #     total_duration = "{:02d}시간 {:02d}분".format(hours, minutes)
    #     return total_duration
    
class Comment(models.Model):
    pass