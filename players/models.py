import urllib
import json
from django.db import models
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from push_notifications.models import GCMDevice, APNSDevice

# Create your models here.

class SingleRelatedObjectDescriptorReturnsNone(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(SingleRelatedObjectDescriptorReturnsNone, self).__get__(instance=instance, instance_type=instance_type)
        except ObjectDoesNotExist:
            return None

class OneToOneOrNoneField(models.OneToOneField):
    """A OneToOneField that returns None if the related object doesn't exist"""
    related_accessor_class = SingleRelatedObjectDescriptorReturnsNone

class Player(models.Model):
    user = models.ForeignKey(User)
    has_it = models.BooleanField(default = False)
    started_with_it = models.BooleanField(default = False)
    last_got_it = models.DateTimeField(null = True, blank = True)
    last_gave_it = models.DateTimeField(null = True, blank = True)
    parent = models.ForeignKey('self', related_name='child', blank=True, null=True)
    lat = models.FloatField(null = True, blank = True)
    lon = models.FloatField(null = True, blank = True)
    gave_it_lat = models.FloatField(null = True, blank = True)
    gave_it_lon = models.FloatField(null = True, blank = True)
    generation = models.IntegerField(default = 0)
    gcmdevice = OneToOneOrNoneField(GCMDevice, blank=True, null=True)
    apnsdevice = OneToOneOrNoneField(APNSDevice, blank=True, null=True)
    descendants = models.IntegerField(default = 0)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Player.objects.create(user = instance)
