from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, User
from django.db.models.fields import TextField
from django.conf import settings
from accounts.helpers import random_digit


class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.TextField(max_length=200, blank=True, null=True)
    is_verify = models.BooleanField(default=False)
    #is_verifeid

class Otp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(default=random_digit, max_length=5)
    is_verify = models.BooleanField(default=False)




