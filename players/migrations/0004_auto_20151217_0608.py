# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import players.models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20151217_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='apnsdevice',
            field=players.models.OneToOneOrNoneField(null=True, blank=True, to='push_notifications.APNSDevice'),
        ),
        migrations.AlterField(
            model_name='player',
            name='gcmdevice',
            field=players.models.OneToOneOrNoneField(null=True, blank=True, to='push_notifications.GCMDevice'),
        ),
    ]
