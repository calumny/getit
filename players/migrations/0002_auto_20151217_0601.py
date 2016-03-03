# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import players.models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='apnsdevice',
            field=players.models.OneToOneOrNoneField(to='push_notifications.APNSDevice'),
        ),
        migrations.AlterField(
            model_name='player',
            name='gcmdevice',
            field=players.models.OneToOneOrNoneField(to='push_notifications.GCMDevice'),
        ),
    ]
