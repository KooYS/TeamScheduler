import requests
import json
import logging
from schedule import views
from django.conf import settings


# Get an instance of a logger
logger = logging.getLogger(__name__)
def find(auth,teamcode):
	photourl = views.findPhoto(teamcode)
	data = {}
	headers = {'Authorization': 'Bearer %s' % auth}
	arguments = {'template_id':{'9502'},'template_args':json.dumps({'title':teamcode+"팀",'content':"팀플 시간이 얼마 남지 않았습니다.","path":"static/img/"+photourl})}
	logger.error(requests.post("https://kapi.kakao.com/v1/user/me", headers=headers).text)
	print(arguments)
	resp = requests.post("https://kapi.kakao.com/v2/api/talk/memo/send", headers=headers, data=arguments)
	print("response status:\n%d" % resp.status_code)
	print("response headers:\n%s" % resp.headers)
	print("response body:\n%s" % resp.text)
# def find(auth):
# 	headers = {'Authorization': 'Bearer %s' % auth}
# 	arguments = {'template_object' : {
# 	  "object_type": "feed",
# 	  "content": {
# 	    "title": "카카오톡 링크 4.0",
# 	    "description": "디폴트 템플릿 FEED",
# 	    "image_url": "http://k.kakaocdn.net/dn/RY8ZN/btqgOGzITp3/uCM1x2xu7GNfr7NS9QvEs0/kakaolink40_original.png",
# 	    "link": {
# 	      "web_url": "https://developers.kakao.com",
# 	      "mobile_web_url": "https://developers.kakao.com"
# 	    }
# 	  },
# 	  "social": {
# 	    "like_count": 100,
# 	    "comment_count": 200
# 	  },
# 	  "button_title": "바로 확인"
# 	}}
# 	resp = requests.post("https://kapi.kakao.com/v2/api/talk/memo/default/send", headers=headers, data=arguments)
# 	print("response status:\n%d" % resp.status_code)
# 	print("response headers:\n%s" % resp.headers)
# 	print("response body:\n%s" % resp.text)