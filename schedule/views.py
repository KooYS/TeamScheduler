from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from schedule.models import User
from schedule.models import TeamInfo
from schedule.form import PostForm
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import requests
import numpy as np
import re, os
import base64
from django.conf import settings
from everytime.find_empty_room import empty
from everytime.studyroom import parse_studyroom

logger = logging.getLogger(__name__)

# 컴퓨터 소프트웨어 개발의 구조적 패턴 중 MTV 컨트롤러 부분. 
# 사용자는 컨트롤러를 사용하여 모델의 상태를 바꾼다. 모델의 상태가 바뀌면 모델은 등록된 뷰에 자신의 상태가 바뀌었다는 것을 알리고 뷰는 거기에 맞게 사용자에게 모델의 상태를 보여 준다.
# 뷰는 templates이다.(html 파일)

# oauth
# 사용자에게 알람(나에게 보내기)를 위하여 access_token을 받는 작업이다.
# 카카오톡 api를 직접적으로 다루는 컨트롤러이다. 카카오톡 아이디와 팀코드에 해당하는 user에 access_token를 저장한다.
def oauth(request):
	if request.method == "GET" and 'code' in request.GET:
		url = "https://kauth.kakao.com/oauth/token"
		payload = {"grant_type" : "authorization_code", "client_id" : "21755e7ccf4a9d96914cdecf96701018" , "redirect_uri" : settings.MAIN_URL+"oauth" , "code" : str(request.GET['code'])}
		response = requests.post(url,data=payload)
		access_token = json.loads(((response.text).encode('utf-8')))['access_token']
		userinfo = request.GET['state'].split(':')
		user = User.objects.get(kakao_id=userinfo[1],teamcode=userinfo[0])
		user.alarm_token = access_token
		user.save()
		return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

	state = request.session['teamcode']+':'+request.session['kakao_id']
	return render(request,"html/oauth.html" , {'redirect_uri' : settings.MAIN_URL+"oauth", 'state' : state})

# success 
# 작업이 끝날때 완료했다는 페이지를 보여주는 컨트롤러
def success(request):
	return render(request,"html/success.html")

# teamschedule
# request.session에 각 유저의 시간표를 합쳐서 팀의 스케쥴표가 나오면 이 스케쥴의 정보를 유저에게 보여주기 위해서 만들어진 컨트롤러이다. teamschedule 뷰에서 trigger로 form의 정보가 submit되고 그 때 팀 시간표가 html2canvas으로 이미지화시켜서 다시 이 컨트롤러로 넘어와서 TeamInfo 모델에 저장한다.
def teamschedule(request,kakao_id):
	if request.method == "POST":
		savePhoto(request.POST['timetableurl'],request.POST['teamcode'])
		teaminfo = TeamInfo.objects.get(teamcode = request.POST['teamcode'])
		teaminfo.timetablehtml = request.POST['timetable_html']
		teaminfo.save()
		return redirect('oauth')

	return render(request, 'html/teamschedule.html',{'kakao_id' : kakao_id,'range' : range(0,7)})

# selectofAlarm
# 알람설정 버튼을 눌렀을때 해당 카카오톡 아이디에 여러 팀프로젝트가 존재할 수 있다. 이때 자신이 참여한 모든 팀프로젝트의 리스트를 보여주는 컨트롤러이다.
# 이 해당 뷰에서는 setofAlarm으로 넘겨준다.
def selectofAlarm(request,kakao_id):
	teaminfos = TeamInfo.objects.filter(kakao_id_list__icontains=kakao_id)
	teamcode_list = ""
	for teaminfo in teaminfos:
		teamcode_list = teamcode_list + "/" + teaminfo.teamcode
	return render(request,"html/alarm_select.html",{'kakao_id' : kakao_id,'teamcodes' : teamcode_list})


# setofAlarm
# 사용자가 참여한 팀프젝트 리스트 중 하나를 선택하면 알람받을 시간을 설정하고 몇 분전에 그 알람을 받을지를 골라서 저장하여 알람 스케쥴을 저장하는 작업을 하는 컨트롤러이다. 
def setofAlarm(request,teamcode):

	teaminfo = TeamInfo.objects.get(teamcode=teamcode)
	if request.method == "POST":
		teaminfo.alarm_data = request.POST['alarm_data']
		teaminfo.alarm_data_before_time = request.POST['time']
		teaminfo.save()
		return render(request,"html/success.html")

	return render(request,"html/alarm.html",{'teamcode' : teamcode , 'html' : teaminfo.timetablehtml})

# index
# 가장 처음에 시간표를 설정하는 컨트롤러. 여기서 teamschedule로 지금까지 저장된 같은 팀코드의 시간표를 자신의 시간표와 합쳐서 보낸다.
def index(request,kakao_id):
	if request.method == "POST":
		request.session['kakao_id'] = kakao_id
		request.session['teamcode'] = request.POST['teamcode']
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			#post.author = request.user
			user = User.objects.filter(kakao_id=kakao_id,teamcode = post.teamcode)
			if user:
				user = User.objects.get(kakao_id=kakao_id,teamcode = post.teamcode)
				user.published_date = timezone.now()
				user.schedule_data = post.schedule_data
				user.timetableurl = post.timetableurl
				user.save()
			else:
				post.kakao_id = kakao_id
				post.published_date = timezone.now()
				post.save()

			row = 15
			col = 5
			users = User.objects.filter(teamcode=post.teamcode)
			request.session['count'] = 0
			result = np.zeros((row, col),dtype=int);
			teaminfo = TeamInfo.objects.filter(teamcode=post.teamcode)
			if not teaminfo:
				teaminfo = TeamInfo(teamcode = post.teamcode , kakao_id_list = "")
				teaminfo.save()
			
			teaminfo = TeamInfo.objects.get(teamcode = post.teamcode)
			for user in users:
				if not kakao_id in teaminfo.kakao_id_list:
					teaminfo.kakao_id_list = teaminfo.kakao_id_list+"/"+kakao_id
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
			#logger.error(''.join(map(str,result)))
			request.session['schedule_data'] = result
			teaminfo.schedule_data = result
			teaminfo.save()
			request.session['teamcode'] = post.teamcode
			return redirect('teamschedule',kakao_id=kakao_id)
		#return redirect('teamschedule',kakao_id=kakao_id)

	#user = User.objects.all()
	return render(request, 'html/index.html', {'range' : range(0,7)})

# keyboard
# 카카오톡의 api 중 스마트채팅에서 버튼을 보여주기 위한 컨트롤러.
def keyboard(request):
	return JsonResponse({'type' : 'buttons','buttons' : ['시간표 설정','알고리즘','알람설정','팀플룸보기']})

# foo(추가적인 작업이 있을 수 도 있어서 임시로 foo라는 이름으로 정함)
# 카카오톡 아이디에 해당하는 팀 코드의 시간표를 보여주기 위한 함수
# 현재 하나의 프로젝트 사진만 보여주기때문에 다수의 팀프로젝트의 사진은 보여주지 못하여 수정이 필요한 상황.
def foo(kakao_id):
	getTeamcode = User.objects.filter(kakao_id=kakao_id)
	return findPhoto(getTeamcode.first().teamcode)

# message
# 카카오톡 api 중 스마트채딩 버튼을 눌렀을 때 그 버튼의 해당하는 작업을 진행하기 위해 만들어진 컨트롤러.
# 시간표 설정 - index로 연결해준다.
# 알고리즘(버튼 이름 수정 해야함)- 해당 아이디의 팀 시간표를 사진으로 보여준다. 그로인해서 사용자는 사진을 저장 및 확인 할 수 있다.
# 알람설정 - 자신이 알람을 받고자 한다면 자신의 팀코드에 해당하는 시간표의 알람시간을 설정하여 알람을 받는다.(나에게 보내기)
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
			 "message_button": {"label": "시간표 설정", "url": settings.MAIN_URL+"id/"+return_json_str['user_key']}
			 },
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘','알람설정','팀플룸보기']}
		})
	if return_str == "알고리즘":
		photourl = foo(request.session['kakao_id'])
		#logger.error(request.session['kakao_id'])
		#logger.error(settings.MAIN_URL+photourl)
		return JsonResponse({ 
			'message': {"text" : "", "photo" : {"url" : settings.MAIN_URL+"static/img/"+photourl, "width" : 630,"height" : 720},"message_button": {"label": "크게 보기","url": settings.MAIN_URL+"static/img/"+photourl}},
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘','알람설정','팀플룸보기']}
		})
	if return_str == "알람설정":
		return JsonResponse({ 
			'message': {'text': "설정하기",
			 "message_button": {"label": "알람설정", "url": settings.MAIN_URL+"alarm/"+return_json_str['user_key']+"/"}
			 },
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘','알람설정','팀플룸보기']}
		})

	if return_str == "팀플룸보기":
		#parse_studyroom()
		#print(empty())
		return JsonResponse({ 
			'message': {'text': "팀플룸보기",
			 "message_button": {"label": "팀플룸보기", "url": settings.MAIN_URL+"room/"}
			 },
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘','알람설정','팀플룸보기']}
		})


# room
# 팀플하는 시간에 맞춰서 사용할 수 있는 팀플룸의 정보를 보여준다. 학교 팀플룸, 빈강의실에 대한 정보 
def room(request):

	return render(request, 'html/room.html', {'empty_room' : empty() , 'img_path' : settings.MAIN_URL+'static/img/'+'studyroom_time.png'})

# findPhoto
# 팀코드의 시간표 사진을 찾는 함수. 로컬루트에 저장된 사진의 이름을 가져온다. 이는 message의 알고리즘 부분에서 받아서 링크를 보내준다.(해당 서버)  
def findPhoto(teamcode):
	uploaded_filename = teamcode+".png"
	preventchange = uploaded_filename
	full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)
	for x in range(0,100):
		image_index = "%d_" % x
		if not os.access(full_filename, os.W_OK):
			break;
		returnvalue = preventchange
		preventchange = uploaded_filename = image_index + uploaded_filename
		full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)
		uploaded_filename = teamcode+".png"

	return returnvalue


# savePhoto
# 팀코드의 시간표 사진을 로컬 루트에 저장한다. 사진이 바뀌면 바뀐 이미지가 카카오톡에 노출되야 하는데 이부분은 카카오톡의 에러가 있어서 사진이 바뀌면 새로운 이름으로 저장된다. 예시) %d_teamcode.png
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

	for x in range(0,100):
		image_index = "%d_" % x
		if not os.access(full_filename, os.W_OK):
			break
		uploaded_filename = image_index + uploaded_filename
		full_filename = os.path.join(settings.MEDIA_ROOT,uploaded_filename)
		returnvalue = uploaded_filename
		uploaded_filename = teamcode+".png"

	#logger.error(full_filename)
	with open(full_filename, 'wb') as f:
		f.write(image_data)

	return returnvalue

