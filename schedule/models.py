from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	teamcode = models.CharField(max_length=20)
	created_date = models.DateTimeField(default=timezone.now)
	kakao_id = models.CharField(max_length=60)
	schedule_data = models.CharField(max_length=100 ,null=True) 

	def __str__(self):
		return self.teamcode