# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos'),
        ),
    ]
