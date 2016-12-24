# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-24 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_entry_views_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewerMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
