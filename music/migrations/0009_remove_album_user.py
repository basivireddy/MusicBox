# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 19:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_album_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='user',
        ),
    ]
