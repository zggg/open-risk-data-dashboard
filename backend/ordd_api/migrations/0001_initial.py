# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 07:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ordd_api.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso2', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_reviewed', models.BooleanField(default=False)),
                ('review_date', models.DateTimeField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('is_existing', models.BooleanField()),
                ('is_existing_txt', models.CharField(blank=True, max_length=256)),
                ('is_digital_form', models.BooleanField()),
                ('is_avail_online', models.BooleanField()),
                ('is_avail_online_meta', models.BooleanField()),
                ('is_bulk_avail', models.BooleanField()),
                ('is_machine_read', models.BooleanField()),
                ('is_machine_read_txt', models.CharField(blank=True, max_length=256)),
                ('is_pub_available', models.BooleanField()),
                ('is_avail_for_free', models.BooleanField()),
                ('is_open_licence', models.BooleanField()),
                ('is_open_licence_txt', models.CharField(blank=True, max_length=256)),
                ('is_prov_timely', models.BooleanField()),
                ('is_prov_timely_last', models.CharField(blank=True, max_length=128)),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordd_api.Country')),
            ],
        ),
        migrations.CreateModel(
            name='KeyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='KeyDataset',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=256, unique=True)),
                ('resolution', models.CharField(blank=True, max_length=32)),
                ('format', models.CharField(blank=True, max_length=32)),
                ('comment', models.CharField(blank=True, max_length=1024)),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='KeyDatasetName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('category', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyPeril',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='KeyTagGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OptIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=ordd_api.models.my_random_key, max_length=16)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256)),
                ('institution', models.CharField(blank=True, max_length=256)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, max_length=4096)),
            ],
        ),
        migrations.AddField(
            model_name='keytag',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='ordd_api.KeyTagGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='keydatasetname',
            unique_together=set([('name', 'category')]),
        ),
        migrations.AddField(
            model_name='keydataset',
            name='applicability',
            field=models.ManyToManyField(to='ordd_api.KeyPeril'),
        ),
        migrations.AddField(
            model_name='keydataset',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordd_api.KeyCategory'),
        ),
        migrations.AddField(
            model_name='keydataset',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordd_api.KeyDatasetName'),
        ),
        migrations.AddField(
            model_name='keydataset',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordd_api.KeyLevel'),
        ),
        migrations.AddField(
            model_name='keydataset',
            name='tag_available',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ordd_api.KeyTagGroup'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='keydataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dataset', to='ordd_api.KeyDataset'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dataset',
            name='tag',
            field=models.ManyToManyField(blank=True, to='ordd_api.KeyTag'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='url',
            field=models.ManyToManyField(blank=True, to='ordd_api.Url'),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordd_api.Region'),
        ),
        migrations.AlterUniqueTogether(
            name='keytag',
            unique_together=set([('group', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='keydataset',
            unique_together=set([('category', 'dataset', 'description', 'level'), ('category', 'code')]),
        ),
    ]
