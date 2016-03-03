# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_auto_20151217_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='gave_it_lat',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='player',
            name='gave_it_lon',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
