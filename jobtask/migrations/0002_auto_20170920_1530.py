# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 15:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobtask', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaltMinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=32, verbose_name='IP')),
                ('saltkey', models.CharField(max_length=64, verbose_name='SaltKey')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.AlterField(
            model_name='comm_task_def',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobtask.Task_Def', verbose_name='\u9009\u62e9\u5df2\u5b9a\u4e49\u4efb\u52a1'),
        ),
        migrations.AlterField(
            model_name='task_def',
            name='remote_file',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u670d\u52a1\u5668\u7aef\u6587\u4ef6'),
        ),
    ]
