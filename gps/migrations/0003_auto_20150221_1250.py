# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gps', '0002_auto_20150221_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsnodemetrics',
            name='vin',
            field=models.TextField(max_length=32),
            preserve_default=True,
        ),
    ]
