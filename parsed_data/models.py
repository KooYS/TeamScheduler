from django.db import models

# Create your models here.


class StudyRoomData(models.Model):
    name = models.CharField(max_length=50)
    floor = models.CharField(max_length=5)
    offTime = models.IntegerField(null=True)

    def __str__(self):
        return self.name
