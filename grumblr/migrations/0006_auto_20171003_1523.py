# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_userprofile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grumblr.UserProfile'),
        ),
    ]