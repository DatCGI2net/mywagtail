# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 07:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20170409_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='portfolios',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='services',
        ),
    ]