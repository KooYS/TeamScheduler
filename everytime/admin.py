from django.contrib import admin
from .models import EveryTimeData, ParsedData, ClassPerDate, AllClass


# Register your models here.
admin.site.register(EveryTimeData)
admin.site.register(ParsedData)
admin.site.register(ClassPerDate)
admin.site.register(AllClass)
# admin.site.register(StudyRoomData)