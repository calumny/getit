from players.models import Player, GCMDevice
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import sched, time


class Command(BaseCommand):
    help = 'Resets it for the month, chooses a new device that starts with it, and sends push notifications'

    def start_with_player(self, player):
	player.has_it = True	
	player.save()
	device = player.gcmdevice
	device.send_message("YOU'RE STARTING WITH IT")
	s = sched.scheduler(time.time, time.sleep)
	s.enter(5, 1, self.recheck, (player,))
	s.run()

    def recheck(self, player):
	print("RECHECK")
	recheck_player = Player.objects.get(pk = player.id)
	device = recheck_player.gcmdevice
	print(Player.objects.filter(gcmdevice__active=True).count())
	print(recheck_player.has_it)
	print(recheck_player.lat)
	if recheck_player is None or recheck_player.lat is None or recheck_player.lon is None:
	    device.active = False
	    device.save()
	    recheck_player.has_it = False
	    recheck_player.save()
	    print(Player.objects.filter(gcmdevice__active= True).order_by('?'))
	    player2 = Player.objects.filter(gcmdevice__active= True).order_by('?').first()
	    return self.start_with_player(player2)
	else:
	    recheck_player.started_with_it = True
	    recheck_player.last_got_it = timezone.now()
	    recheck_player.save()
	    return True

    def handle(self, *args, **options):
	Player.objects.all().update(lat = None, lon = None, descendants = 0, generation = 0, has_it = False, started_with_it = False, parent = None)
	player = Player.objects.filter(gcmdevice__active= True).order_by('?').first()
#	player = Player.objects.all()[11]
	self.start_with_player(player)

#	player.has_it = True
#	player.started_with_it = True
#	player.save()
#	device = player.gcmdevice
#	device.send_message("YOU'RE STARTING WITH IT")
