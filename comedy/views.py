from . import NLP
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		message = data['message']

		# follow up query
		if message.isdigit() and len(NLP.follow_term) > 0:
			res = NLP.find_followups(message)
			response['message'] = {'text': res, 'user': False, 'chat_bot': True}
			response['status'] = 'ok'
			NLP.follow_up = {}
			NLP.follow_term = {}
			NLP.request = ""
			NLP.flag = 0
		else:
			# new query
			if NLP.flag == 0:
				state = NLP.find_state(message)
				if state == "None":
					NLP.request += message
					NLP.request += " "
					response['message'] = {'text': "Please enter a valid state!", 'user': False, 'chat_bot': True}
					response['status'] = 'ok'
					NLP.flag = 1
				else:
					res = NLP.findanswer(message)
					response['message'] = {'text': res, 'user': False, 'chat_bot': True}
					response['status'] = 'ok'
			# follow up query for specific state
			else:
				if NLP.find_state(message) !=  "None":
					NLP.request += message
					print(NLP.request)
					res = NLP.findanswer(NLP.request)
					response['message'] = {'text': res, 'user': False, 'chat_bot': True}
					response['status'] = 'ok'
					NLP.request = ""
					NLP.flag = 0
				else:
					response['message'] = {'text': "Please enter a valid state!", 'user': False, 'chat_bot': True}
					response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)


def home(request, template_name="home.html"):
	context = {'title': 'Chatbot Version 1.0'}
	return render_to_response(template_name, context)
