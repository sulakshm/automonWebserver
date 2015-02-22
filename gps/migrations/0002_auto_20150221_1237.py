# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsnode',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gpsnode',
            name='lastActive',
            field=models.DateTimeField(auto_now=True, verbose_name=b'LastActive'),
            preserve_default=True,
        ),
    ]
