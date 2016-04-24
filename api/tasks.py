from __future__ import absolute_import

from django.conf import settings
from django.db.models import Q
from celery import shared_task
from django.utils import timezone

from players.models import User, Player, GCMDevice, APNSDevice, Round, Transfer
from api.views import haversinedistance

from datetime import datetime, timedelta

import csv
import operator
import random
import math
import hashlib

@shared_task
def import_sample_data():
    print("IMPORTING DATA")
    with open('/home/sites/getit/static/testDataCZ.csv', 'rb') as csvfile:
        test_data = csv.DictReader(csvfile)
        i = 0
        
        get_it_time = timezone.now()
        players = []

        for row in test_data:
            i += 1
            print row['time']
            print i
            hashname = hashlib.sha1(row['selfid']).hexdigest()[:30]
            hashword =hashlib.sha1(row['selfid']).hexdigest()[:30]
            user = User.objects.create(username = hashname)
            user.set_password(hashword)
            user.save()
            player = Player.objects.get(user = user)
            player.lat = float(row['latitude'])
            player.lon = float(row['longitude'])
            player.last_got_it = get_it_time
            player.has_it = True
            if (i == 1):
                player.started_with_it = True
                player.generation = 0
            else:
                parent = random.choice(players)
                player.parent = parent
                travel_dist = haversinedistance(math.radians(parent.lat), math.radians(player.lat), math.radians(parent.lon), math.radians(player.lon))
                play_round = Round.objects.get(current=True)
                transfer = Transfer.objects.create(from_lat = parent.lat, from_lon = parent.lon, to_lat = player.lat, to_lon = player.lon, from_player = parent, to_player = player, distance = travel_dist, date = player.last_got_it, play_round = play_round)
                print "TRANSFER "
                print travel_dist
            get_it_time = get_it_time + timedelta(minutes=1)
            player.save()
            print "SAVED PLAYER"
            print player.id
            players.append(player)


@shared_task
def start_with_player(player_id):
	print("STARTING TASK")
        player =  Player.objects.get(pk = player_id)
	if (player.has_it == True and (player.lat is None or player.lon is None)):
		print("PLAYER {pk} DIDN'T RETURN LOCATION".format(pk=player.id))
		player.has_it = False
		player.save()
                device = None
                if player.gcmdevice is not None:
		    device = player.gcmdevice
                else:
                    device = player.apnsdevice
		device.active = False
		device.save()
		player = Player.objects.filter(Q(apnsdevice__active=True) | Q(gcmdevice__active= True)).order_by('?').first()		
		start_with_player.apply_async(args=(player.id,), countdown=1)
		print("CALLED TASK WITH NEW PLAYER")
	elif player.has_it == True:
                player.last_got_it = timezone.now()
                player.started_with_it = True
                player.save()
		print("PLAYER {pk} HAS IT".format(pk=player.id)) 
		return True
	else:
		print("GIVING IT TO PLAYER {pk}".format(pk=player.id))
		print("TESTING PRINT")
		player.has_it = True
        	player.save()
        	print("SAVED PLAYER")
                if player.gcmdevice is not None:
    		    device = player.gcmdevice
        	    device.send_message("YOU'RE STARTING WITH IT")
                else:
                    device = player.apnsdevice
                    device.send_message(None, content_available=True, extra={"task": "get_location"})
		print("SENT MESSAGE")
		start_with_player.retry(countdown=5)
		print("TRYING SAME PLAYER")
@shared_task
def reset_it():
        reset_time = timezone.now()
        last_round = Round.objects.get(current=True)
        last_round.end_date = reset_time
        prev_number = last_round.number
        last_round.save()
        Round.objects.all().update(current=False)
        new_round = Round.objects.create(number = prev_number + 1, current = True, start_date = reset_time)
 	Player.objects.all().update(lat = None, lon = None, descendants = 0, generation = 0, has_it = False, started_with_it = False, parent = None)
        player = Player.objects.filter(Q(apnsdevice__active=True) | Q(gcmdevice__active= True)).order_by('?').first()
#       player = Player.objects.all()[11]
        start_with_player.delay(player.id)
