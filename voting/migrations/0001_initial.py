# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-22 00:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('votee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votee', to=settings.AUTH_USER_MODEL)),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]