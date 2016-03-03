# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0007_auto_20160204_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('current', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('from_lat', models.FloatField(null=True, blank=True)),
                ('from_lon', models.FloatField(null=True, blank=True)),
                ('to_lat', models.FloatField(null=True, blank=True)),
                ('to_lon', models.FloatField(null=True, blank=True)),
                ('from_player', models.ForeignKey(related_name='from_transfer', to='players.Player')),
                ('play_round', models.ForeignKey(to='players.Round')),
                ('to_player', models.ForeignKey(related_name='to_transfer', to='players.Player')),
            ],
        ),
    ]
