import urllib
import json
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class Player(models.Model):
    user = models.ForeignKey(User)
    has_it = models.BooleanField(default = False)
    started_with_it = models.BooleanField(default = False)
    last_got_it = models.DateTimeField(null = True, blank = True)
    last_gave_it = models.DateTimeField(null = True, blank = True)
    parent = models.ForeignKey('self', related_name='child', blank=True, null=True)
    lat = models.FloatField(null = True, blank = True)
    lon = models.FloatField(null = True, blank = True)
    generation = models.IntegerField(null = True, blank = True)
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Player.objects.create(user = instance)