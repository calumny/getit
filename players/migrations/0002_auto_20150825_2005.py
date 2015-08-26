# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='generation',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='last_gave_it',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='last_got_it',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='lat',
            field=models.FloatField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='lon',
            field=models.FloatField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
