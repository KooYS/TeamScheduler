import requests
import json
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
def find(auth):
	data = {}
	headers = {'Authorization': 'Bearer %s' % auth}
	template_id = 9502 # 메시지 템플릿 v2의 아이디
	params = {"template_id": {template_id}}

	# logger.error(requests.post("https://kapi.kakao.com/v1/user/me", headers=headers).text)
	resp = requests.post("https://kapi.kakao.com/v2/api/talk/memo/send", headers=headers, data=params)
	# print("response status:\n%d" % resp.status_code)
	# print("response headers:\n%s" % resp.headers)
	# print("response body:\n%s" % resp.text)

