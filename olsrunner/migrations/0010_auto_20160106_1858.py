# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 23:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olsrunner', '0009_week_startdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='L0game1time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L0game2time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L0game3time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L1game1time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L1game2time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L1game3time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L2game1time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L2game2time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L2game3time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L3game1time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L3game2time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='week',
            name='L3game3time',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
