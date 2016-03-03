# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0006_auto_20160204_0523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='apnsdevice',
            field=models.OneToOneField(null=True, blank=True, to='push_notifications.APNSDevice'),
        ),
        migrations.AlterField(
            model_name='player',
            name='gcmdevice',
            field=models.OneToOneField(null=True, blank=True, to='push_notifications.GCMDevice'),
        ),
    ]
