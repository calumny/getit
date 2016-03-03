from players.models import Player, GCMDevice, APNSDevice
from django.core.management.base import BaseCommand, CommandError

import time

class Command(BaseCommand):
    help = 'Reactivates GCMDevices'

    def handle(self, *args, **options):
	GCMDevice.objects.all().update(active = True)
	APNSDevice.objects.all().update(active = True)
