# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 13:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobtask', '0012_auto_20170926_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='create_use',
            new_name='create_user',
        ),
    ]