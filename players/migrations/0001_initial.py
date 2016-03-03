# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import players.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('push_notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_it', models.BooleanField(default=False)),
                ('started_with_it', models.BooleanField(default=False)),
                ('last_got_it', models.DateTimeField(null=True, blank=True)),
                ('last_gave_it', models.DateTimeField(null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('generation', models.IntegerField(default=0)),
                ('descendants', models.IntegerField(default=0)),
                ('apnsdevice', players.models.OneToOneOrNoneField(blank=True, to='push_notifications.APNSDevice')),
                ('gcmdevice', players.models.OneToOneOrNoneField(blank=True, to='push_notifications.GCMDevice')),
                ('parent', models.ForeignKey(related_name='child', blank=True, to='players.Player', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
