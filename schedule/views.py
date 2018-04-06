from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import User
from .form import PostForm
from django.views.decorators.csrf import csrf_exempt
import json
import logging

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
			#post.published_date = timezone.now()
			#logger.error('Something went wrong!')
			post.save()
			return redirect('index' , kakao_id = kakao_id )

	user = User.objects.all()
	text = "시간표 등록 전"

	if( 'form_message' in request.session ):
		text = request.session['form_message']
		del request.session['form_message']

	return render(request, 'html/index.html', {'users' : user , 'test' : text})

def keyboard(request):
	return JsonResponse({'type' : 'buttons','buttons' : ['시간표 설정','알고리즘']})

def foo(kakao_id):
	getTeamcode = User.objects.filter(kakao_id=kakao_id)
	users = User.objects.filter(teamcode=getTeamcode.first().teamcode)
	text = ""
	for user in users:
		# 알고리즘 작성 부분
		text = text+"\n"+user.schedule_data
		logger.error(user.schedule_data)
	return text

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
		return JsonResponse({
			'message': {'text': foo(return_json_str['user_key']),
			},
			'keyboard': {'type': 'buttons','buttons': ['시간표 설정','알고리즘']}
		})
