# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20170807_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
