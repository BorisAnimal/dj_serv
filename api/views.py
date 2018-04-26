from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseBadRequest

from rest_framework.authtoken.models import Token

from api.models import Accounts, Applets

import re, traceback, json, requests

import requests

sockets_server = 'http://10.240.18.136:5000'
applets_list_url = sockets_server + '/getlist'
send_to_applet_url = sockets_server + '/sendDataToApplet'

ERROR = 'error_msg'

@csrf_exempt
def signup(request):
	req = get_headers(request)
	if request.method == 'POST':
		print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
		print(request.POST)
		print(request.POST['login'])
		login = request.POST['login']
		password = request.POST['password']
		if login is None or password is None:
			return HttpResponseBadRequest(content='Empty field!')
		print('login: {}\npassword: {}'.format(login, password))
		user = User(username=login)
		user.set_password(password)
		user.save()
		return JsonResponse({})
	else:
		return HttpResponseBadRequest(content="Incorrect request type")

@csrf_exempt
def change_master_password(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		return HttpResponseBadRequest(content='incorrect TOKEN')
	npass = req['PASSWORD']
	if npass :
		user.set_password(npass)
	else: 
		return HttpResponseBadRequest(content='incorrect TOKEN')
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
		return HttpResponseBadRequest(content='incorrect TOKEN')
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
		return HttpResponseBadRequest(content='incorrect TOKEN')
	#Database request
	accs = Accounts.objects.filter(owner_id=user.id)
	apps = Applets.objects.filter(owner_id=user.id)

	apps_count = apps.count()
	accs_count = accs.count()

	accs.delete()
	apps.delete()

	resp['applets_deleted'] = apps_count
	resp['accounts_deleted'] = accs_count

	return JsonResponse(resp)

# Invokes request to other server
def applets_descriptions(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		return HttpResponseBadRequest(content='incorrect TOKEN')
	#Sockserv request
	r = requests.get(applets_list_url, params={'login':user.username})
	print(r.text)
	l = r.json()['results']
	print(l)

	return JsonResponse(l, safe=False)


@csrf_exempt
def send_data_to_applet(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		resp[ERROR] = 'incorrect TOKEN'
		return HttpResponseBadRequest(content='incorrect TOKEN')
	#Select
	try: 
		acc_id = request.POST['accountID']
		app_id = request.POST['appletID']
		print('acc: {}\napp: {}'.format(acc_id, app_id))
	except:
		print('wrong fields')
		return HttpResponseBadRequest(content='Wrong fields')
	#Send
	try:
		acc = Accounts.objects.get(owner_id=user, id=acc_id) #.values('login', 'password')
		r = requests.post(send_to_applet_url, data={'appletid':app_id, 'login': acc.login, 'pass': acc.password})
	except:
		print('wrong values')
		resp[ERROR] = 'wrong values'

	return JsonResponse(resp)

def get_account(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		return HttpResponseBadRequest(content='incorrect TOKEN')
	#Database access
	acc = Accounts.objects.get(owner_id=user, id=req['ACCOUNTID'])
	resp = {
	'id': acc.id,
	'description': acc.description,
	'password': acc.password,
	'login': acc.login,
	}
	return JsonResponse(resp)


def accounts_descriptions(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		return HttpResponseBadRequest(content='incorrect TOKEN')
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
		return HttpResponseBadRequest(content='incorrect TOKEN')

	#TODO: handle fields empty errors.

	print(request.POST)
	print(request.POST['login'])
	login = request.POST['login']
	password = request.POST['password']
	if login is None or password is None:
		return HttpResponseBadRequest(content='Empty field!')
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

@csrf_exempt
def delete_account(request):
	resp = {ERROR: ''}
	req = get_headers(request)
	print('\nHELLO>>>>>>>>>>>>>>>>>>>>\n')
	try:
		user = get_user_from_token(req['TOKEN'])
	except ObjectDoesNotExist as e:
		return HttpResponseBadRequest(content='incorrect TOKEN')

	print(request.POST)
	acc_id = request.POST['accountID']
	acc = Accounts.objects.get(owner_id=user, id=acc_id)
	acc.delete()

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
