from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BotEnv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, blank=False) # name: uid_name
    path = models.CharField(max_length=500, blank=False)

class BotItem(models.Model):
    env = models.ForeignKey(BotEnv, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, blank=False) # name: uid_eid_name
    path = models.CharField(max_length=500, blank=False)
    
