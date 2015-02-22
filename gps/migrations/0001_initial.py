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
            name='GpsNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ident', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lastActive', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GpsNodeMetrics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vin', models.TextField()),
                ('vinCached', models.NullBooleanField(default=None)),
                ('latitude', models.DecimalField(max_digits=14, decimal_places=12)),
                ('longitude', models.DecimalField(max_digits=14, decimal_places=12)),
                ('accuracy', models.FloatField()),
                ('speed', models.FloatField()),
                ('altitude', models.FloatField()),
                ('nsTimestamp', models.BigIntegerField()),
                ('bearing', models.FloatField()),
                ('node', models.ForeignKey(to='gps.GpsNode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
