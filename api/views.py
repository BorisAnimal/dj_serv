from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

from rest_framework.authtoken.models import Token

import json

from api.models import Accounts
from api.models import Applets

import re
import traceback

ERROR = 'error_msg'


@csrf_exempt
def change_master_password(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		resp[ERROR] = 'incorrect TOKEN'
		return JsonResponse(resp)
	npass = req['PASSWORD']
	if npass :
		user.set_password(npass)
	else: 
		resp[ERROR] = 'new password not set!'
		return JsonResponse(resp)
	accounts =  json.loads(request.body)
	print(accounts)
	for tmp in accounts:
		try:
			acc = Accounts.objects.filter(owner_id=user.id, id=tmp['id'])[0]
			print("Was\npass: {}\nlogin: {}\nBecame\npass: {}\nlogin: {}\n".format(acc.password, acc.login, tmp['password'], tmp['login']))
			acc.password = tmp['password']
			acc.login = tmp['login']
			acc.save()
		except:
			print("Error while changing Master password!\npas: {}\nlogin: {}".format(tmp.password, tmp.login))
			traceback.print_exc()
	return JsonResponse(resp)




@csrf_exempt
def dump_all_from_account(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		resp[ERROR] = 'incorrect TOKEN'
		return JsonResponse(resp)
	#Database request
	accs = Accounts.objects.filter(owner_id=user.id).values('id', 'description', 'login', 'password')
	#Parsing of the request
	values = []
	for i in accs:
		values.append(i)

	return JsonResponse(values, safe=False)


@csrf_exempt
def wipe_all_from_account(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		resp[ERROR] = 'incorrect TOKEN'
		return JsonResponse(resp)
	#Database request
	accs = Accounts.objects.filter(owner_id=user.id)
	apps = Applets.objects.filter(owner_id=user.id)

	apps_count = apps.count()
	accs_count = accs.count()

	accs.delete()
	apps.delete()

	resp['applets_deleted'] = apps
	resp['accounts_deleted'] = accs

	return JsonResponse(resp)


@csrf_exempt
def send_data_to_applet(request):
	pass


def register_applet(request):
	pass


def applets_descriptions(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		resp[ERROR] = 'incorrect TOKEN'
		return JsonResponse(resp)
	#Database request
	instance = Applets.objects.filter(owner_id=user.id).values('description', 'id')
	#Parsing of the request
	values = []
	for i in instance:
		values.append(i)

	return JsonResponse(values, safe=False)


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
