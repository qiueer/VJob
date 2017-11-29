# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-22 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comm_Job_Def',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobtype', models.IntegerField(default=2, verbose_name='\u4efb\u52a1\u7c7b\u578b')),
                ('func', models.TextField(verbose_name='\u529f\u80fd\u8bf4\u660e')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'comm_job_def',
            },
        ),
        migrations.CreateModel(
            name='Comm_Task_Def',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasktype', models.IntegerField(default=2, verbose_name='\u4efb\u52a1\u7c7b\u578b')),
                ('params', models.TextField(blank=True, null=True, verbose_name='\u53c2\u6570')),
                ('iphosts', models.TextField(verbose_name='IP\u6216\u4e3b\u673a\u540d')),
                ('exe_user', models.CharField(max_length=64, verbose_name='\u6267\u884c\u7528\u6237')),
                ('timeout', models.IntegerField(verbose_name='\u8d85\u65f6\u65f6\u95f4')),
                ('func', models.TextField(verbose_name='\u529f\u80fd\u8bf4\u660e')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'comm_task_def',
            },
        ),
        migrations.CreateModel(
            name='CommJobTaskConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('comm_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobtask.Comm_Job_Def')),
                ('comm_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobtask.Comm_Task_Def')),
            ],
            options={
                'db_table': 'comm_job_task_config',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobid', models.CharField(max_length=64, verbose_name='\u4f5c\u4e1a\u5355\u53f7')),
                ('create_dt', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('create_user', models.CharField(max_length=64, null=True, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('job_status', models.SmallIntegerField(verbose_name='\u4f5c\u4e1a\u72b6\u6001')),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='Job_SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_loc', models.SmallIntegerField(blank=True, default=1, verbose_name='\u6587\u4ef6\u4f4d\u7f6e')),
                ('file', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6587\u4ef6\u8def\u5f84')),
                ('main_script_name', models.CharField(default='', max_length=64, verbose_name='\u4e3b\u6267\u884c\u7a0b\u5e8f')),
                ('params', models.TextField(verbose_name='\u53c2\u6570')),
                ('executor', models.CharField(max_length=16, verbose_name='\u89e3\u6790\u5668')),
                ('exe_user', models.CharField(max_length=16, verbose_name='\u6267\u884c\u7528\u6237')),
                ('iphost', models.TextField(verbose_name='IP\u6216\u4e3b\u673a\u540d')),
                ('create_dt', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('task_status', models.SmallIntegerField(blank=True, null=True, verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('retcode', models.SmallIntegerField(blank=True, null=True, verbose_name='\u6267\u884c\u8fd4\u56de\u7801')),
                ('stdout', models.TextField(blank=True, null=True, verbose_name='\u6807\u51c6\u8f93\u51fa')),
                ('stderr', models.TextField(blank=True, null=True, verbose_name='\u6807\u51c6\u9519\u8bef\u8f93\u51fa')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'job_subtask',
            },
        ),
        migrations.CreateModel(
            name='Job_Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_loc', models.SmallIntegerField(default=1, verbose_name='\u6587\u4ef6\u4f4d\u7f6e')),
                ('file', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6587\u4ef6\u8def\u5f84')),
                ('main_script_name', models.CharField(default='', max_length=64, verbose_name='\u4e3b\u6267\u884c\u7a0b\u5e8f')),
                ('params', models.TextField(verbose_name='\u53c2\u6570')),
                ('iphosts', models.TextField(verbose_name='IP\u6216\u4e3b\u673a\u540d')),
                ('exe_user', models.CharField(max_length=64, verbose_name='\u6267\u884c\u7528\u6237')),
                ('timeout', models.IntegerField(verbose_name='\u8d85\u65f6\u65f6\u95f4')),
                ('fromip', models.CharField(max_length=16, verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('job_task_status', models.SmallIntegerField(blank=True, null=True, verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
                ('comm_task', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comm_tasks', to='jobtask.Comm_Task_Def', verbose_name='\u4efb\u52a1\u5b9a\u4e49')),
                ('job', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_tasks', to='jobtask.Job', verbose_name='\u4f5c\u4e1a')),
            ],
            options={
                'db_table': 'job_task',
            },
        ),
        migrations.CreateModel(
            name='JobClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobclass', models.CharField(max_length=32, verbose_name='\u4f5c\u4e1a\u5206\u7c7b')),
                ('jobclass_cn', models.CharField(max_length=32, verbose_name='\u4f5c\u4e1a\u5206\u7c7b(CN)')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'job_class',
            },
        ),
        migrations.CreateModel(
            name='JobStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobstatus', models.CharField(max_length=32, verbose_name='\u4f5c\u4e1a\u72b6\u6001')),
                ('jobstatus_cn', models.CharField(max_length=32, verbose_name='\u4f5c\u4e1a\u72b6\u6001(CN)')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'job_status',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobtype', models.CharField(max_length=32, verbose_name='\u4f5c\u4e1a\u7c7b\u578b')),
                ('jobtype_cn', models.CharField(max_length=32, verbose_name='\u4f5c\u4e1a\u7c7b\u578b(CN)')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'job_type',
            },
        ),
        migrations.CreateModel(
            name='Res_Control_Conf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mem', models.IntegerField(verbose_name='\u5185\u5b58\u8981\u6c42(M)')),
                ('mem_percent', models.IntegerField(verbose_name='\u5185\u5b58\u8981\u6c42(%)')),
                ('sys_load_1', models.FloatField(verbose_name='\u7cfb\u7edf\u8d1f\u8f7d\u8981\u6c42(1m)')),
                ('sys_load_5', models.FloatField(verbose_name='\u7cfb\u7edf\u8d1f\u8f7d\u8981\u6c42(5m)')),
                ('sys_load_15', models.FloatField(verbose_name='\u7cfb\u7edf\u8d1f\u8f7d\u8981\u6c42(15m)')),
            ],
            options={
                'db_table': 'res_control_conf',
            },
        ),
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
            options={
                'db_table': 'saltminion',
            },
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_loc', models.SmallIntegerField(blank=True, default=1, verbose_name='\u6587\u4ef6\u4f4d\u7f6e')),
                ('file', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u6587\u4ef6\u8def\u5f84')),
                ('main_script_name', models.CharField(default='', max_length=64, verbose_name='\u4e3b\u6267\u884c\u7a0b\u5e8f')),
                ('params', models.TextField(verbose_name='\u53c2\u6570')),
                ('executor', models.CharField(max_length=16, verbose_name='\u89e3\u6790\u5668')),
                ('exe_user', models.CharField(max_length=16, verbose_name='\u6267\u884c\u7528\u6237')),
                ('iphost', models.TextField(verbose_name='IP\u6216\u4e3b\u673a\u540d')),
                ('create_dt', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('task_status', models.SmallIntegerField(blank=True, null=True, verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('retcode', models.SmallIntegerField(blank=True, null=True, verbose_name='\u6267\u884c\u8fd4\u56de\u7801')),
                ('stdout', models.TextField(blank=True, null=True, verbose_name='\u6807\u51c6\u8f93\u51fa')),
                ('stderr', models.TextField(blank=True, null=True, verbose_name='\u6807\u51c6\u9519\u8bef\u8f93\u51fa')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'subtask',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskid', models.CharField(max_length=64, null=True, verbose_name='\u4efb\u52a1\u53f7')),
                ('exe_user', models.CharField(max_length=64, verbose_name='\u6267\u884c\u7528\u6237')),
                ('params', models.TextField(verbose_name='\u53c2\u6570')),
                ('iphosts', models.TextField(verbose_name='IP\u6216\u4e3b\u673a\u540d')),
                ('timeout', models.IntegerField(default=0, verbose_name='\u8d85\u65f6\u65f6\u95f4')),
                ('fromip', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('task_status', models.SmallIntegerField(blank=True, null=True, verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('create_user', models.CharField(blank=True, max_length=64, null=True, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.CreateModel(
            name='Task_Def',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_loc', models.SmallIntegerField(blank=True, verbose_name='\u6587\u4ef6\u4f4d\u7f6e')),
                ('file', models.FileField(blank=True, null=True, upload_to='upload/%Y/%m/%d', verbose_name='\u672c\u5730\u6587\u4ef6')),
                ('remote_file', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u670d\u52a1\u5668\u7aef\u6587\u4ef6')),
                ('file_type', models.SmallIntegerField(verbose_name='\u6587\u4ef6\u7c7b\u578b')),
                ('main_script_name', models.CharField(max_length=64, verbose_name='\u4e3b\u6267\u884c\u7a0b\u5e8f')),
                ('params', models.TextField(verbose_name='\u53c2\u6570')),
                ('executor', models.CharField(max_length=16, verbose_name='\u89e3\u6790\u5668')),
                ('func', models.TextField(verbose_name='\u529f\u80fd\u8bf4\u660e')),
                ('task_status', models.SmallIntegerField(verbose_name='\u4efb\u52a1\u72b6\u6001')),
                ('task_type', models.SmallIntegerField(verbose_name='\u4efb\u52a1\u7c7b\u578b')),
                ('task_perm_status', models.SmallIntegerField(verbose_name='\u4efb\u52a1\u6743\u9650\u72b6\u6001')),
                ('create_user', models.CharField(max_length=64, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_dt', models.DateTimeField(blank=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
                ('res_ctl_conf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobtask.Res_Control_Conf', verbose_name='\u4e3b\u673a\u8d44\u6e90\u63a7\u5236')),
            ],
            options={
                'db_table': 'task_def',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='taskdef',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='jobtask.Task_Def', verbose_name='\u9009\u62e9\u5df2\u5b9a\u4e49\u4efb\u52a1'),
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='jobtask.Task', verbose_name='\u4f5c\u4e1a\u4efb\u52a1'),
        ),
        migrations.AddField(
            model_name='job_subtask',
            name='jobtask',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='job_sub_tasks', to='jobtask.Job_Task', verbose_name='\u4f5c\u4e1a\u4efb\u52a1'),
        ),
        migrations.AddField(
            model_name='job',
            name='job_class',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobtask.JobClass', verbose_name='\u4f5c\u4e1a\u5206\u7c7b'),
        ),
        migrations.AddField(
            model_name='job',
            name='jobdef',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobtask.Comm_Job_Def', verbose_name='\u4f5c\u4e1a'),
        ),
        migrations.AddField(
            model_name='comm_task_def',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comm_task_defs', to='jobtask.Task_Def', verbose_name='\u9009\u62e9\u5df2\u5b9a\u4e49\u4efb\u52a1'),
        ),
        migrations.AddField(
            model_name='comm_job_def',
            name='comm_tasks',
            field=models.ManyToManyField(through='jobtask.CommJobTaskConfig', to='jobtask.Comm_Task_Def', verbose_name='\u4efb\u52a1\u5217\u8868'),
        ),
        migrations.AddField(
            model_name='comm_job_def',
            name='job_class',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobtask.JobClass', verbose_name='\u4f5c\u4e1a\u5206\u7c7b'),
        ),
        migrations.AddField(
            model_name='comm_job_def',
            name='job_status',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobtask.JobStatus', verbose_name='\u4f5c\u4e1a\u72b6\u6001'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['jobid'], name='jobid_idx'),
        ),
    ]
