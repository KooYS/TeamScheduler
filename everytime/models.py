from django.db import models


# Create your models here.
class EveryTimeData(models.Model):
    crawling_data = models.CharField(max_length=100)

    def __str__(self):
        return self.crawling_data


class ParsedData(models.Model):
    schedule_parsing = models.CharField(max_length=100)

    def __str__(self):
        return self.schedule_parsing


class AllClass(models.Model):
    exist_class = models.CharField(max_length=300, default=None)
    building_name = models.CharField(max_length=20, default=None)
    floor = models.CharField(max_length=20, default=None)

    def __str__(self):
        title = self.building_name + '\t' + self.floor + '층'
        return title


class ClassPerDate(models.Model):
    date_name = models.CharField(max_length=10)
    class_data = models.CharField(max_length=30, default=None)

    def __str__(self):
        return self.date_name

# class StudyRoomData(models.Model):
#     name = models.CharField(max_length=50)
#     floor = models.CharField(max_length=5)
#     offTime = models.IntegerField(null=True)

#     def __str__(self):
#         return self.name
