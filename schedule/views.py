from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import User
from .form import PostForm
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import numpy as np
import re, os
import base64
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request,kakao_id):
	if request.method == "POST":
		request.session['form_message'] = "시간표 관련 db작업이 이뤄진 후"
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			#post.author = request.user
			post.kakao_id = kakao_id
			# imgstr = re.search(r'base64,(.*)', request.POST['timetableurl']).group(1)
			# output = open('output.png', 'wb')
			# output.write(imgstr.decode('base64'))
			# output.close()
			#post.published_date = timezone.now()
			#logger.error('Something went wrong!')
			post.save()
			return redirect('index' , kakao_id = kakao_id )

	user = User.objects.all()
	text = "시간표 등록 전"
	#foo("L9SSEpG8aEcG1")

	if( 'form_message' in request.session ):
		text = request.session['form_message']
		del request.session['form_message']

	#form = PostForm()
	return render(request, 'html/index.html', {'users' : user , 'test' : text , 'range' : range(0,7)})


def keyboard(request):
	return JsonResponse({'type' : 'buttons','buttons' : ['시간표 설정','알고리즘']})

def foo(kakao_id):
	#grabzIt.HTMLToImage("<html><body><h1>Hello World!</h1></body></html>")
	getTeamcode = User.objects.filter(kakao_id=kakao_id)
	users = User.objects.filter(teamcode=getTeamcode.first().teamcode)
	result = np.zeros((16, 5),dtype=int);
	for user in users:
		text = user.schedule_data.split(',')
		text = list(map(int, text))
		text = np.array(text).reshape(16,5)
		#logger.error(text)
		result = np.add(result, text)
		#text = text+"\n"+user.schedule_data
		#logger.error(user.schedule_data)
		#logger.error(result)
		#logger.error("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
		#logger.error(getTeamcode.first().timetableurl)
	return savePhoto(getTeamcode.first().timetableurl,kakao_id)

@csrf_exempt
def message(request):
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']
	request.session['kakao_id'] = return_json_str['user_key']
	#'message': {'text': "you type "+return_str+"!"},
	if return_str == "시간표 설정":
		return JsonResponse({
			'message': {'text': "링크 클릭",
			 "message_button": {"label": "시간표 설정", "url": "http://112.171.53.22:1111/"+"id/"+return_json_str['user_key']}
			 },
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘']}
		})
	if return_str == "알고리즘":
		photourl = foo(request.session['kakao_id'])
		logger.error(photourl)
		return JsonResponse({ 
			'message': {"text" : "", "photo" : {"url" : "http://112.171.53.22:1111/static/img/"+photourl, "width" : 630,"height" : 720},"message_button": {"label": "크게 보기","url": "http://112.171.53.22:1111/static/img/"+photourl}},
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘']}
		})

def savePhoto(image_string,kakao_id):
	dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
	image_data = image_string#request.POST['timetableurl']
	image_data = dataUrlPattern.match(image_data).group(2)
	image_data = image_data.encode()
	image_data = base64.b64decode(image_data)
	
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT, folder))
	except:
		pass
	uploaded_filename = returnvalue = kakao_id+".png"
	full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)

	for x in range(0,10):
		image_index = "%d_" % x
		if not os.access(full_filename, os.W_OK):
			break;
		uploaded_filename = image_index + uploaded_filename
		full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)
		returnvalue = uploaded_filename
		uploaded_filename = kakao_id+".png"

	logger.error(full_filename)
	with open(full_filename, 'wb') as f:
		f.write(image_data)

	return returnvalue

