from players.models import Player, GCMDevice, APNSDevice
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db.models import Q

import sched, time

from api.tasks import reset_it

class Command(BaseCommand):
    help = 'Resets it for the month, chooses a new device that starts with it, and sends push notifications'

    def start_with_player(self, player):
	player.has_it = True
        player.started_with_it = True
        player.last_got_it = timezone.now()	
	player.save()
	if player.gcmdevice is not None:
		device = player.gcmdevice
		device.send_message("YOU'RE STARTING WITH IT")
	else:
		device = player.apnsdevice
		device.send_message(None, content_available=True, extra={"task": "get_location"})
	s = sched.scheduler(time.time, time.sleep)
	s.enter(5, 1, self.recheck, (player,))
	s.run()

    def recheck(self, player):
	print("RECHECK")
        print("PRINT TEST")
	recheck_player = Player.objects.get(pk = player.id)
	device = None
	if player.gcmdevice is not None:
		print("GCM DEVICE")
		device = recheck_player.gcmdevice
	else:
		print("APNS DEVICE")
		device = recheck_player.apnsdevice
	print("ACTIVE DEVICES: %d" % Player.objects.filter(Q(gcmdevice__active= True) | Q(apnsdevice__active=True)).count())
	print("HAS IT: %d" % recheck_player.has_it)
	print(recheck_player.lat)
	if recheck_player.lat is None or recheck_player.lon is None:
#	    device.active = False
#	    device.save()
	    recheck_player.has_it = False
#            recheck_player.started_with_it = False
#            recheck_player.last_got_it = None
	    recheck_player.save()
	    print(Player.objects.filter(Q(gcmdevice__active= True) | Q(apnsdevice__active=True)).order_by('?'))
	    player2 = Player.objects.filter(Q(apnsdevice__active= True) | Q(apnsdevice__active=True)).order_by('?').first()
	    if player2 is not None:
		return self.start_with_player(player2)
	    else:
		print("NOBODY GOT IT")
		return False
	else:
	    return True

    def handle(self, *args, **options):
        reset_it()
#	Player.objects.all().update(lat = None, lon = None, descendants = 0, generation = 0, has_it = False, started_with_it = False, parent = None)
#	player = Player.objects.filter(Q(apnsdevice__active= True) | Q(apnsdevice__active=True)).order_by('?').first()
#	player = Player.objects.all()[11]
#	self.start_with_player(player)

#	player.has_it = True
#	player.started_with_it = True
#	player.save()
#	device = player.gcmdevice
#	device.send_message("YOU'RE STARTING WITH IT")
