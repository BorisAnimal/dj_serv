from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Accounts(models.Model):
	owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
	login = models.CharField(max_length=256)
	password = models.CharField(max_length=256)
	description = models.CharField(max_length=256)

class Applets(models.Model):
	owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=256)
	ip = models.CharField(max_length=256)
