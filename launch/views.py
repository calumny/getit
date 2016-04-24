from django.shortcuts import render

from django.core.urlresolvers import reverse
from django import template

from players.models import Round, Player, Transfer

from django.db.models import Sum

# Create your views here.
def main(request):
    player = Player.objects.exclude(last_got_it__isnull=True).filter(has_it=True).order_by('last_got_it').last()
    last_got_it = player.last_got_it
    current_round = Round.objects.get(current=True)
    has_it_count = Player.objects.filter(has_it=True).count()
    started_with_it = Player.objects.filter(started_with_it=True).count()
    distance = int(Transfer.objects.filter(play_round = current_round).aggregate(Sum('distance'))['distance__sum'])
    if distance is None:
        distance = 0
    minutes = int((last_got_it - current_round.start_date).total_seconds()/60)
    stats = {"has_it_count":has_it_count, "distance":distance, "minutes":minutes}
    return render(request, 'launch/getit.html', context=stats)
