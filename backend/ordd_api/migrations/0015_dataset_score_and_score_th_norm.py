# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-07 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordd_api', '0014_migrate_content_to_v9'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='score_th_norm',
            field=models.FloatField(default=0.0),
        ),
    ]