from players.models import Player, GCMDevice, APNSDevice
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db.models import Q

import sched, time

from api.tasks import import_sample_data

class Command(BaseCommand):
    help = 'Resets it for the month, chooses a new device that starts with it, and sends push notifications'

    def handle(self, *args, **options):
        import_sample_data()
#	Player.objects.all().update(lat = None, lon = None, descendants = 0, generation = 0, has_it = False, started_with_it = False, parent = None)
#	player = Player.objects.filter(Q(apnsdevice__active= True) | Q(apnsdevice__active=True)).order_by('?').first()
#	player = Player.objects.all()[11]
#	self.start_with_player(player)

#	player.has_it = True
#	player.started_with_it = True
#	player.save()
#	device = player.gcmdevice
#	device.send_message("YOU'RE STARTING WITH IT")
