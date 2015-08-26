# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('has_it', models.BooleanField(default=False)),
                ('started_with_it', models.BooleanField(default=False)),
                ('last_got_it', models.DateTimeField()),
                ('last_gave_it', models.DateTimeField()),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('generation', models.IntegerField()),
                ('parent', models.ForeignKey(null=True, related_name='child', blank=True, to='players.Player')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
