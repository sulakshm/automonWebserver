# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gps', '0005_auto_20150221_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsnodemetrics',
            name='vin',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
    ]
