# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-18 15:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordd_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='applicability',
        ),
    ]