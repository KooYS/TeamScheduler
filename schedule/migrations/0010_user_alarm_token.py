# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-19 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_auto_20180519_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='alarm_token',
            field=models.TextField(null=True),
        ),
    ]
