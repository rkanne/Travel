# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 20:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travelbuddy', '0004_auto_20161021_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='join',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='join', to='travelbuddy.Trips'),
        ),
    ]
