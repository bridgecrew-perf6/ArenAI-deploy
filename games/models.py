from enum import Flag
from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.db.models.base import ModelState
from botenv.models import BotItem
# Create your models here.

class Submission(models.Model):
    bot = models.ForeignKey(BotItem, on_delete=models.CASCADE)
    exec_path = models.CharField(max_length=500, blank=False)
    game_name = models.CharField(max_length=100, blank=False)
    score = models.IntegerField(default=0)
