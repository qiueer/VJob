# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20170807_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateTimeField(),
        ),
    ]
