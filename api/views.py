from django.shortcuts import render
from datetime import datetime, timedelta
import json
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django import template
from django.utils.six import BytesIO
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils import timezone
import math
from django.dispatch import receiver


from rest_framework.authtoken.models import Token

register = template.Library()

from django.contrib.auth import authenticate, login, logout, get_user

from django.contrib.auth.models import User

from players.models import Player

from push_notifications.models import GCMDevice, APNSDevice

#from gcm.signals import device_registered

# Create your views here.

#@receiver(device_registered)
#def handle_gcm_registration(sender, **kwargs):
#    device = kwargs.get("device")
#    request = kwargs.get("request")
#    if request.user.is_authenticated:
#	user = request.user
#	player = Player.objects.get(user = user)
#	player.gcmdevice = device
#	player.save()

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def add_generation(current_generation, generation_number, generations_list):
    next_generation = Player.objects.filter(parent__in = current_generation) 
    generation_count = next_generation.count()
    if (generation_count == 0):
        return generations_list
    else:
        generations_list.append({"generation":generation_number, "count":generation_count})
        return add_generation(next_generation, generation_number + 1, generations_list)
   
def increment_descendants(player):
    player.descendants = player.descendants + 1
    if (player.descendants == 100 or player.descendants == 1000 or player.descendants == 10000):
	device = player.gcmdevice
	device.send_message(player.descendants + " people got it because of you!")
    player.save()
    if player.generation == 0:
        return True
    else:
	return increment_descendants(player.parent)
 
@api_view(['GET'])
def get_generations(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        generations_list = []
        generations_list = add_generation([player], 0, generations_list)
        return JSONResponse(generations_list)
    return JSONResponse([])

@api_view(['POST'])
def confirm_location(request):
    if request.user.is_authenticated():
	user = request.user
	player = Player.objects.get(user = user)
	if player.has_it and player.lat is None and player.lon is None:
	    player.lat = request.data['lat']
	    player.lon = request.data['lon']
#	    f = open('lat_lon.txt', 'w')
#	    f.write("location")
#	    f.write(request.data['lat'])
#	    f.write(request.data['lon'])
	    player.save()
	    return JSONResponse(True)
    return JSONResponse(False)

@api_view(['POST'])    
def give_it(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        if player.has_it:
            player.last_gave_it = timezone.now()
            player.lat = request.data['lat']
            player.lon = request.data['lon']
            player.save()
            return JSONResponse(True)
    return JSONResponse(False)

from players.models import GCMDevice

@api_view(['GET'])    
def did_i_give_it(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        children = player.child.all().count()
        return JSONResponse(children)
    return JSONResponse(0)

@api_view(['GET'])    
def count(request):
    return JSONResponse(Player.objects.filter(has_it=True).count())

@api_view(['GET'])    
def status(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        print(player.has_it)
	print(player.id)
	return JSONResponse(player.has_it)
    return JSONResponse(False)
        
@api_view(['POST'])
def get_it(request):
        user = request.user
        player = Player.objects.get(user = user)
        if not player.has_it:
            time_threshold = timezone.now() - timedelta(seconds=5)
            recently_gave = Player.objects.filter(last_gave_it__gt=time_threshold, has_it=True)
            lat = request.data['lat']
            lon = request.data['lon']
            player.lat = lat
            player.lon = lon
            player.save()


	    for giver in recently_gave:
		deltaLat = math.radians(abs(giver.lat - lat))
		deltaLon = math.radians(abs(giver.lon - lon))
		print(deltaLat)
		print(deltaLon)
		x = deltaLon * math.cos(math.radians(lat))
		print(x)
		R = 6371000
		dist = R * math.sqrt(math.pow(x, 2) + math.pow(deltaLat, 2))
		print(dist)

                if dist < 1000:

                    player.parent = giver

		    player.generation = giver.generation + 1

		    player.last_got_it = timezone.now()

		    player.has_it = True

		    player.save()
                    return JSONResponse(increment_descendants(giver))            
            return JSONResponse(False)
        else:
            return JSONResponse(True)
                
@api_view(['POST'])
def register(request):
    if request.user.is_authenticated():
	return JSONResponse({'message' : 'That user has already been registered'})
    else:
        user = User.objects.create(username = request.data['username'])
	user.set_password(request.data['password'])
        user.save()
    	token = Token.objects.get(user = user)
   	return JSONResponse({'key':token.key})
   
@api_view(['POST'])
def set_gcm_token(request):
    if request.user.is_authenticated():
	user = request.user
	player = Player.objects.get(user = user)
	gcmdevice = GCMDevice.objects.create(registration_id = request.data['key'])
	gcmdevice.save()
	player.gcmdevice = gcmdevice
	player.save() 
	return JSONResponse(True)
    return JSONResponse(False)        

@api_view(['POST'])
def set_apns_token(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        apnsdevice = APNSDevice.objects.create(registration_id = request.data['key'])
        apnsdevice.save()
        player.apnsdevice = apnsdevice
        player.save()
        return JSONResponse(True)
    return JSONResponse(False)

        
@api_view(['POST'])
def get_token(request):
    user = User.objects.get(username = request.data['username'])
    token = Token.objects.get(user = user)
    return JSONResponse({'key':token.key})
    
                
        
