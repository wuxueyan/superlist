# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-17 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_item_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(default=b'888888'),
        ),
    ]
