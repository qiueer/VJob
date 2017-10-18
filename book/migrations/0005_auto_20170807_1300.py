# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20170807_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='\u90ae\u7bb1'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='website',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
