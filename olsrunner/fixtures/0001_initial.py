# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.IntegerField(default=0)),
                ('team2', models.IntegerField(default=0)),
                ('winner', models.IntegerField(default=0)),
                ('filename', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlayerIGN', models.CharField(max_length=30)),
                ('PlayerName', models.CharField(max_length=50)),
                ('IsCaptain', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamID', models.IntegerField(default=0)),
                ('teamName', models.CharField(max_length=100)),
                ('Captain', models.CharField(max_length=20)),
                ('Player1', models.CharField(max_length=20)),
                ('Player2', models.CharField(max_length=20)),
                ('Player3', models.CharField(max_length=20)),
                ('Player4', models.CharField(max_length=20)),
            ],
        ),
    ]
