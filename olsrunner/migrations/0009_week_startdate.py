# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 23:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olsrunner', '0008_auto_20160106_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='startdate',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
