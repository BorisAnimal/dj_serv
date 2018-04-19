from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

from rest_framework.authtoken.models import Token

from api.models import Accounts
from api.models import Applets

import re

ERROR = 'error_msg'


def accounts_descriptions(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		resp[ERROR] = 'incorrect TOKEN'
		return JsonResponse(resp)
	#Database request
	instance = Accounts.objects.filter(owner_id=user.id).values('description', 'id')
	#Parsing of the request
	values = []
	for i in instance:
		values.append(i)

	return JsonResponse(values, safe=False)


@csrf_exempt
def add_account(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		resp[ERROR] = 'incorrect TOKEN'
		return JsonResponse(resp)

	#TODO: handle fields empty errors.

	print(request.POST)
	print(request.POST['login'])
	login = request.POST['login']
	password = request.POST['password']
	if not (login or password):
		resp[ERROR] = 'empty password or login'
		return JsonResponse(resp)
	description = ''
	if 'description' in request.POST:
		description = request.POST['description']
	if 'id' in request.POST:
		acc_id = request.POST['id']
		acc = Accounts.objects.get(owner_id=user, id=acc_id)
		acc.login = login
		acc.description = description
		acc.password = password
	else:
		acc = Accounts(owner_id=user, login=login, password=password, description=description)
	acc.save()

	return JsonResponse({})


def get_headers(request):
	"""
		Blackbox from:
		https://stackoverflow.com/questions/3889769/how-can-i-get-all-the-request-headers-in-django?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
	"""
	regex = re.compile('^HTTP_')

	return dict((regex.sub('', header), value) for (header, value) in request.META.items() if header.startswith('HTTP_'))


def get_user_from_token(token):
	"""
		WARNING!!! throws ObjectDoesNotExist
	"""
	user = Token.objects.get(key=token).user
	return user
