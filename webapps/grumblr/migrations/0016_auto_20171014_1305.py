# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 17:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0015_auto_20171014_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 14, 17, 5, 43, 123242, tzinfo=utc)),
        ),
    ]