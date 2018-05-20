from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	teamcode = models.CharField(max_length=20)
	created_date = models.DateTimeField(default=timezone.now)
	kakao_id = models.CharField(max_length=60)
	schedule_data = models.CharField(max_length=200 ,null=True) 
	timetableurl = models.TextField(null=True)
	alarm_token = models.TextField(null=True)
	def __str__(self):
		return self.teamcode


class TeamInfo(models.Model):
	teamcode = models.CharField(max_length=20)
	kakao_id_list = models.TextField(null=True)
	schedule_data = models.CharField(max_length=200 ,null=True) 
	alarm_data = models.CharField(max_length=200 ,null=True) 
	alarm_data_before_time = models.CharField(max_length=20,null=True)
	timetablehtml = models.TextField(null=True)
	def __str__(self):
		return self.teamcode