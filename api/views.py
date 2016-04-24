from django.shortcuts import render
from datetime import datetime, timedelta
import hashlib
import json
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django import template
from django.utils.six import BytesIO
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from django.utils import timezone
import math
from django.dispatch import receiver
from django.db.models import Sum

from rest_framework.authtoken.models import Token
from rest_framework_csv.renderers import CSVRenderer

register = template.Library()

from django.contrib.auth import authenticate, login, logout, get_user

from django.contrib.auth.models import User

from players.models import Player, Round, Transfer

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

def haversine(theta):
    return (1-math.cos(theta))/2.0

def haversinedistance(theta1, theta2, lambda1, lambda2):
    r = 3959
    return 2*r*math.asin(math.sqrt(haversine(theta2-theta1)+math.cos(theta1)*math.cos(theta2)*haversine(lambda2-lambda1)))

def find_furthest_descendant(player, current_generation, current_furthest_dist):
    next_generation = Player.objects.filter(parent__in = current_generation)
    if (next_generation.count() == 0):
        return current_furthest_dist
    else:
        for child in next_generation:
            dist = haversinedistance(player.gave_it_lat, child.lat, player.gave_it_lon, child.lon)
            if dist > current_furthest_dist:
                player.furthest_descendant = child
                player.save()
                return find_furthest_descendant(player, next_generation, dist)

@api_view(['GET'])
def get_furthest_descendant(request):    
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        furthest_dist = find_furthest_descendant(player, [player], 0)
        return JSONResponse({"distance":furthest_dist, "lat":player.furthest_descendant.lat, "lon":player.furthest_descendant.lon})
    else:
        return HttpResponse('Unauthorized', status=401)

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
    else:
        return HttpResponse('Unauthorized', status=401)

class MapRenderer (CSVRenderer):
    header = ['lat', 'lon', 'last_got_it', 'id', 'parent']

@api_view(['GET'])
def get_map_locations(request):
#    west = request.data['west']
#    east = request.data['east']
#    south = request.data['south']
#    north = request.data['north']
#    players = Player.objects.filter(has_it=True, lon__gte=west, lon__lte=east, lat__gte=south, lat__lte=north)
    players = Player.objects.filter(has_it=True)
    data = players.values_list('lat', 'lon', 'last_got_it', 'id', 'parent')
#    data = serializers.serialize('json', players, fields=('lat', 'lon', 'last_got_it', 'id', 'parent'))
#    content = [{'lat': player.lat, 'lon':player.lon, 'last_got_it':player.last_got_it, 'id':player.id, 'parent':player.parent} for player in players]
#    return Response(content)
    return JSONResponse(data)

@api_view(['POST'])
def confirm_location(request): 
    if request.user.is_authenticated():
	user = request.user
	player = Player.objects.get(user = user)
#	if player.has_it and (player.lat is None or player.lon is None):
        player.lat = request.data['lat']
        player.lon = request.data['lon']
#	    f = open('lat_lon.txt', 'w')
#	    f.write("location")
#	    f.write(request.data['lat'])
#	    f.write(request.data['lon'])
        player.save()
        return JSONResponse(True)
#        else:
#            return JSONResponse(False)
    else:
        return HttpResponse('Unauthorized', status=401)

@api_view(['POST'])    
def give_it(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        if player.has_it:
            player.last_gave_it = timezone.now()
            player.gave_it_lat = request.data['lat']
            player.gave_it_lon = request.data['lon']
            player.save()
            return JSONResponse(True)
        else:
            return JSONResponse(False)
    else:
        return HttpResponse('Unauthorized', status=401)

from players.models import GCMDevice

@api_view(['GET'])    
def did_i_give_it(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        children = player.child.all().count()
        return JSONResponse(children)
    else:
        return HttpResponse('Unauthorized', status=401)

@api_view(['GET'])
def countdown(request):
    player = Player.objects.filter(has_it=True).order_by('last_got_it').last()
    last_got_it = player.last_got_it
    reset_date = last_got_it + timedelta(days=14)    
    return JSONResponse(reset_date)

@api_view(['GET'])
def get_stats(request):
    player = Player.objects.exclude(last_got_it__isnull=True).filter(has_it=True).order_by('last_got_it').last()
    last_got_it = player.last_got_it
    reset_date = last_got_it + timedelta(days=14)
    current_round = Round.objects.get(current=True)
    has_it_count = Player.objects.filter(has_it=True).count()
    started_with_it = Player.objects.filter(started_with_it=True).count()
    distance = Transfer.objects.filter(play_round = current_round).aggregate(Sum('distance'))['distance__sum']
    if distance is None:
        distance = 0
    time_elapsed = (last_got_it - current_round.start_date).total_seconds()
    mph = distance/time_elapsed * 3600
    players_per_second = (has_it_count - started_with_it)/((timezone.now()-current_round.start_date).total_seconds())
    stats = {"reset_date":reset_date, "has_it_count":has_it_count, "distance":distance, "mph":mph, "players_per_second":players_per_second}
    return JSONResponse(stats)


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
    else:
        return HttpResponse('Unauthorized', status=401)

        
@api_view(['POST'])
def get_it(request):
    if request.user.is_authenticated():
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
		deltaLat = math.radians(abs(giver.gave_it_lat - lat))
		deltaLon = math.radians(abs(giver.gave_it_lon - lon))
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

                    travel_dist = haversinedistance(math.radians(giver.lat), math.radians(player.lat), math.radians(giver.lon), math.radians(player.lon))
                    play_round = Round.objects.get(current=True)
                    transfer = Transfer.objects.create(from_lat = giver.lat, from_lon = giver.lon, to_lat = player.lat, to_lon = player.lon, from_player = giver, to_player = player, distance = travel_dist, date = player.last_got_it, play_round = play_round)

                    return JSONResponse(increment_descendants(giver))            
            return JSONResponse(False)
        else:
            return JSONResponse(True)
    else:
        return HttpResponse('Unauthorized', status=401)

                
@api_view(['POST'])
def register(request):
    if request.user.is_authenticated():
	return JSONResponse({'message' : 'That user has already been registered'})
    else:
        hashname = hashlib.sha1(request.data['username']).hexdigest()[:30]
        hashword =hashlib.sha1(request.data['password']).hexdigest()[:30]
        user = User.objects.create(username = hashname)
	user.set_password(hashword)
        user.save()
    	token = Token.objects.get(user = user)
   	return JSONResponse({'key':token.key})
   
@api_view(['POST'])
def set_gcm_token(request):
    if request.user.is_authenticated():
	user = request.user
	player = Player.objects.get(user = user)
        try:
            gcmdevice = GCMDevice.objects.get(registration_id = request.data['key'])
            gcmdevice.delete()
        except ObjectDoesNotExist:
            pass
        gcmdevice = GCMDevice.objects.create(registration_id = request.data['key'])
        gcmdevice.active =  True
        gcmdevice.player = player
	gcmdevice.save()
        player.gcmdevice = gcmdevice
        player.save()
        return JSONResponse(True)
    else:
        return HttpResponse('Unauthorized', status=401)
   

@api_view(['POST'])
def set_apns_token(request):
    if request.user.is_authenticated():
        user = request.user
        player = Player.objects.get(user = user)
        try:
            apnsdevice = APNSDevice.objects.get(registration_id = request.data['key'])
            apnsdevice.delete()
        except ObjectDoesNotExist:
            pass
        apnsdevice = APNSDevice.objects.create(registration_id = request.data['key'])
        apnsdevice.active =  True
        apnsdevice.player = player
        apnsdevice.save()
        player.apnsdevice = apnsdevice
        player.save()
        return JSONResponse(True)
    else:
        return HttpResponse('Unauthorized', status=401)

@api_view(['POST'])
def get_token(request):
    hashname= hashlib.sha1(request.data['username']).hexdigest()[:30]
    try:
        user = User.objects.get(username = hashname)
    except User.DoesNotExist:
        return HttpResponse('No such user', status=404)
    token = Token.objects.get(user = user)
    return JSONResponse({'key':token.key})
    
                
        
