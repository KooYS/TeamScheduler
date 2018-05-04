from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	teamcode = models.CharField(max_length=20)
	created_date = models.DateTimeField(default=timezone.now)
	kakao_id = models.CharField(max_length=60)
	schedule_data = models.CharField(max_length=200 ,null=True) 
	timetableurl = models.TextField(null=True)
	#photo = models.ImageField(upload_to=settings.IMAGE_UPLOAD_PATH)

	def __str__(self):
		return self.teamcode