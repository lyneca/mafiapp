# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-24 12:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_vote_is_cancel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 24, 23, 11, 44, 368236)),
        ),
    ]
