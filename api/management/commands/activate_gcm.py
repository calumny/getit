from players.models import Player, GCMDevice
from django.core.management.base import BaseCommand, CommandError

import time

class Command(BaseCommand):
    help = 'Reactivates GCMDevices'

    def handle(self, *args, **options):
	GCMDevice.objects.all().update(active = True)

