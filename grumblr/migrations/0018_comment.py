# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 17:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0017_auto_20171014_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemid', models.IntegerField()),
                ('content', models.CharField(max_length=42)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
