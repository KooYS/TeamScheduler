import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
import django
django.setup()
from django.conf.urls import url
from django.conf import settings

from schedule import views

urlpatterns = [
	url(r'^keyboard/', views.keyboard, name='keyboard'),
	url(r'^message',views.message, name='message'),
	url(r'^oauth',views.oauth, name='oauth'),
	url(r'^$',views.success, name='success'),
	url(r'^id/(?P<kakao_id>.+)$', views.index, name='index'),
	url(r'^alarm/(?P<kakao_id>.+)/$', views.selectofAlarm, name='selectofAlarm'),
	url(r'^alarm/(?P<teamcode>.+)$', views.setofAlarm, name='setofAlarm'),
	url(r'^teamschedule/(?P<kakao_id>.+)$', views.teamschedule, name='teamschedule'),
]