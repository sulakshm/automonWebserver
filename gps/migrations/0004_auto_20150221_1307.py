# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gps', '0003_auto_20150221_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsnode',
            name='ident',
            field=models.CharField(max_length=48),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gpsnodemetrics',
            name='vin',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
    ]
