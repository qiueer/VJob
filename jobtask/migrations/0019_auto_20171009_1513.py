# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobtask', '0018_auto_20171008_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtask',
            name='jobtask',
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobtask.Task', verbose_name='\u4f5c\u4e1a\u4efb\u52a1'),
        ),
        migrations.AddField(
            model_name='task',
            name='taskdef',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='jobtask.Task_Def', verbose_name='\u9009\u62e9\u5df2\u5b9a\u4e49\u4efb\u52a1'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comm_task_def',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comm_task_defs', to='jobtask.Task_Def', verbose_name='\u9009\u62e9\u5df2\u5b9a\u4e49\u4efb\u52a1'),
        ),
        migrations.AlterField(
            model_name='job_subtask',
            name='jobtask',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_sub_tasks', to='jobtask.Job_Task', verbose_name='\u4f5c\u4e1a\u4efb\u52a1'),
        ),
    ]
