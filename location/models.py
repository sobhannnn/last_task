from django.db import models
from django.conf import settings
# from accounts.models import MyUser

class LocationUser(models.Model):
    location_lat = models.CharField(max_length=50)
    location_long = models.CharField(max_length=50)
    location_name = models.CharField(default="Hadeth", max_length=50)
    is_finished = models.BooleanField(default=False)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
