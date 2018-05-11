from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
	url(r'^keyboard/', views.keyboard, name='keyboard'),
	url(r'^message',views.message, name='message'),
	url(r'^oauth',views.oauth, name='oauth'),
	url(r'^$',views.success, name='success'),
	url(r'^id/(?P<kakao_id>.+)$', views.index, name='index'),
	url(r'^teamschedule/(?P<kakao_id>.+)$', views.teamschedule, name='teamschedule'),
]