"""ipm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from api import views

from rest_framework.authtoken import views as t_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/check/', t_views.obtain_auth_token), #CheckUser feature
    url(r'^accounts/descriptions/', views.accounts_descriptions), #SelectAccount feature
    url(r'^accounts/', views.add_account), #Add new account to the user's account in system
]

'''
1. users/check/ - good default stuff. Checks if user with provided login and password in system and returns "token" field
else returns "non_field_errors" field with reason.

WARNING!!!1 needs header contains 
    "Content-Type" : "application/json"
and fields like this:
    {
        "username": "abc",
        "password": "qweee123"
    }

returns: 
{
    "token": "{TOKEN_ASSOCIATED_WITH_USER}"
}

2. accounts/descriptions/ - custom. Returns all user's accounts with descriptions. 
WARNING!!!1 needs authorisation token in header
    "token" : "{TOKEN_ASSOCIATED_WITH_USER}"

returns:
if correct authorisation
    [{"description": "Testing, motherfucker", "id": 1}, {"description": "qwewqe", "id": 2}]
else:
    {"error_msg": "incorrect TOKEN"}



3. accounts/ POST message. Receives account data
if 'id' field is present, updates user's account in DB
else creates new

WARNING!!!1 needs authorisation token in header

fields:
'login'
'password'
'description' +-
'id' +-

returns:
{"error_msg": "incorrect TOKEN"}
or {} if all ok

'''


# ^ — начало текста;
# $ — конец текста;
# \d — цифра;
# + — чтобы указать, что предыдущий элемент должен быть повторен как минимум один раз;
# () — для получения части шаблона.