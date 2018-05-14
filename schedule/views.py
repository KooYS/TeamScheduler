from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import User
from .form import PostForm
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import requests
import numpy as np
import re, os
import base64
from django.conf import settings
from .alarm import find

# Get an instance of a logger
mainurl = "http://kooys.pythonanywhere.com/"
#mainurl = "http://112.171.53.22:1111/"

logger = logging.getLogger(__name__)
def oauth(request):
	# if request.method == "POST":
	# 	logger.error(request.POST)
	if request.method == "GET" and 'code' in request.GET:
		url = "https://kauth.kakao.com/oauth/token"
		payload = {"grant_type" : "authorization_code", "client_id" : "21755e7ccf4a9d96914cdecf96701018" , "redirect_uri" : mainurl+"oauth" , "code" : str(request.GET['code'])}
		response = requests.post(url,data=payload)
		access_token = json.loads(((response.text).encode('utf-8')))['access_token']
		find(access_token)
		return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

	return render(request,"html/oauth.html")

def success(request):
	return render(request,"html/success.html")

def teamschedule(request,kakao_id):
	if request.method == "POST":
		logger.error(request.POST['schedule_data'])
		# logger.error(request.POST['teamcode'])
		# #logger.error(request.POST['timetableurl'])
		savePhoto(request.POST['timetableurl'],request.POST['teamcode'])
		# #logger.error(findPhoto(request.POST['teamcode']))
		# return redirect('index',kakao_id=kakao_id)
		return redirect('index',kakao_id=kakao_id)

	return render(request, 'html/teamschedule.html',{'kakao_id' : kakao_id,'range' : range(0,7)})



def index(request,kakao_id):
	request.COOKIES['kakao_id'] = kakao_id
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

			#밑에 전부 주석해제
			post.published_date = timezone.now()
			logger.error('Something went wrong!')
			post.save()
			row = 15
			col = 5
			getTeamcode = User.objects.filter(kakao_id=kakao_id)
			users = User.objects.filter(teamcode=getTeamcode.first().teamcode)
			request.session['count'] = 0
			result = np.zeros((row, col),dtype=int);
			for user in users:
				text = user.schedule_data.split(',')
				text = list(map(int, text))
				text = np.array(text).reshape(row,col)
				result = np.add(result, text)
				request.session['count'] = request.session['count']+1
			result = np.reshape(result,(1 , np.product(result.shape)))
			result = np.asarray(result)
			result = str(result).replace('[[','')
			result = str(result).replace(']]','')
			result = str(result).replace(' ','')
			result = str(result).replace('\n','')
			logger.error(''.join(map(str,result)))
			request.session['schedule_data'] = result
			request.session['teamcode'] = post.teamcode
			return redirect('teamschedule',kakao_id=kakao_id)

	#user = User.objects.all()

	if( 'form_message' in request.session ):
		text = request.session['form_message']
		del request.session['form_message']

	return render(request, 'html/index.html', {'range' : range(0,7)})


def keyboard(request):
	return JsonResponse({'type' : 'buttons','buttons' : ['시간표 설정','알고리즘']})

def foo(kakao_id):
	#grabzIt.HTMLToImage("<html><body><h1>Hello World!</h1></body></html>")
	getTeamcode = User.objects.filter(kakao_id=kakao_id)
	return findPhoto(getTeamcode.first().teamcode)

@csrf_exempt
def message(request):
	mainurl = "http://kooys.pythonanywhere.com/"
	#mainurl = "http://112.171.53.22:1111/"
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']
	request.session['kakao_id'] = return_json_str['user_key']
	#'message': {'text': "you type "+return_str+"!"},
	if return_str == "시간표 설정":
		return JsonResponse({
			'message': {'text': "링크 클릭",
			 "message_button": {"label": "시간표 설정", "url": mainurl+"id/"+return_json_str['user_key']}
			 },
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘']}
		})
	if return_str == "알고리즘":
		photourl = foo(request.session['kakao_id'])
		logger.error(photourl)
		logger.error(request.session['kakao_id'])
		logger.error(mainurl+photourl)
		return JsonResponse({ 
			'message': {"text" : "", "photo" : {"url" : ""+mainurl+photourl, "width" : 630,"height" : 720},"message_button": {"label": "크게 보기","url": mainurl+"static/img/"+photourl}},
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘']}
		})

def findPhoto(teamcode):
	uploaded_filename = teamcode+".png"
	logger.error(uploaded_filename)
	preventchange = ""
	full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)
	logger.error(full_filename)
	for x in range(0,10):
		image_index = "%d_" % x
		if not os.access(full_filename, os.W_OK):
			break;
		returnvalue = preventchange
		preventchange = uploaded_filename = image_index + uploaded_filename
		full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)
		logger.error(full_filename)
		uploaded_filename = teamcode+".png"

	logger.error(returnvalue)
	return returnvalue

def savePhoto(image_string,teamcode):
	dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
	image_data = image_string#request.POST['timetableurl']
	image_data = dataUrlPattern.match(image_data).group(2)
	image_data = image_data.encode()
	image_data = base64.b64decode(image_data)
	
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT, folder))
	except:
		pass
	uploaded_filename = returnvalue = teamcode+".png"
	full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)

	for x in range(0,10):
		image_index = "%d_" % x
		if not os.access(full_filename, os.W_OK):
			break;
		uploaded_filename = image_index + uploaded_filename
		full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)
		returnvalue = uploaded_filename
		uploaded_filename = teamcode+".png"

	logger.error(full_filename)
	with open(full_filename, 'wb') as f:
		f.write(image_data)

	return returnvalue

