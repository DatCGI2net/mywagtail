# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-14 13:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20170414_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientpageplacements',
            name='clientblock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clientblocks', to='home.ClientPageBlock'),
        ),
    ]
