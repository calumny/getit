# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_auto_20151231_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='apnsdevice',
            field=models.ForeignKey(blank=True, to='push_notifications.APNSDevice', null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='gcmdevice',
            field=models.ForeignKey(blank=True, to='push_notifications.GCMDevice', null=True),
        ),
    ]
