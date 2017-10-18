# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

## 资源控制配置表
class Res_Control_Conf(models.Model):
    mem = models.IntegerField(verbose_name="内存要求(M)")
    mem_percent = models.IntegerField(verbose_name="内存要求(%)")
    sys_load_1 = models.FloatField(verbose_name="系统负载要求(1m)")
    sys_load_5 = models.FloatField(verbose_name="系统负载要求(5m)")
    sys_load_15 = models.FloatField(verbose_name="系统负载要求(15m)")

## 任务定义表
class Task_Def(models.Model):
    file = models.FileField(upload_to="upload/%Y/%m/%d", null=True, verbose_name="文件路径")  #文件
    #filepath = models.CharField(max_length=255, verbose_name="文件路径")  #文件
    file_type = models.SmallIntegerField(verbose_name="文件类型")  # 脚本或脚本包
    main_script_name = models.CharField(max_length=64, verbose_name="主脚本名")
    #path = models.CharField(max_length=255, verbose_name="文件路径")
    params = models.TextField(verbose_name="参数")
    executor = models.CharField(max_length=16, verbose_name="解析器")
    func = models.TextField(verbose_name="功能说明")
    task_status = models.SmallIntegerField(verbose_name="任务状态")
    task_type = models.SmallIntegerField(verbose_name="任务类型")
    task_perm_status = models.SmallIntegerField(verbose_name="任务权限状态")
    res_ctl_conf =  models.ForeignKey(Res_Control_Conf, verbose_name="主机资源控制", null=True) 
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间", auto_now=True)
    note = models.TextField(verbose_name="备注")

## 常规任务表，已配置好
class Comm_Task_Def(models.Model):
    task = models.ForeignKey(Task_Def, verbose_name="任务定义")
    func = models.TextField(verbose_name="功能说明")
    exe_user = models.CharField(max_length=64, verbose_name="执行用户") # 在远程主机上执行脚本或任务，主机上的用户
    params = models.TextField(verbose_name="参数")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    iphosts = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    timeout = models.IntegerField(verbose_name="超时时间")
    note = models.TextField(verbose_name="备注") # 在远程主机上执行脚本或任务，主机上的用户
    
## 常规作业表，已配置好
class Comm_Job_Def(models.Model):
    func = models.TextField(verbose_name="功能说明")
    comm_tasks = models.ManyToManyField(Comm_Task_Def, verbose_name="任务列表")
    job_status = models.SmallIntegerField(verbose_name="任务状态")  # 0：停用；1：启用
    job_type = models.SmallIntegerField(verbose_name="任务类型")  # 0：系统作业；2业务作业
    job_perm_status = models.SmallIntegerField(verbose_name="任务权限状态")  # 0：独有不公开  1：所有人可读
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    note = models.TextField(verbose_name="备注")
    
# 创建作业
# 创建任务

# 任务表
class Job(models.Model):
    jobid = models.CharField(max_length=64, verbose_name="作业ID") 
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    job_status =  models.SmallIntegerField(verbose_name="作业状态")   # 0：失败  1：成功  2：等待  3：执行中
    
    class Meta:
        indexes = [
            models.Index(fields=['jobid'], name='jobid_idx'),
        ]
    
class Job_task(models.Model):
    job_id = models.ForeignKey(Job, verbose_name="任务定义")
    task_def_id = models.ForeignKey(Task_Def, verbose_name="任务定义")
    exe_user = models.CharField(max_length=64, verbose_name="执行用户") # 在远程主机上执行脚本或任务，主机上的用户
    params = models.TextField(verbose_name="参数")
    iphosts = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    timeout = models.IntegerField(verbose_name="超时时间")
    fromip = models.CharField(max_length=16, verbose_name="任务状态")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    note = models.TextField(verbose_name="备注")

class Task(models.Model):
    job = models.ForeignKey(Job_task, verbose_name="作业任务")
    params = models.TextField(verbose_name="参数")
    executor = models.CharField(max_length=16, verbose_name="解析器")
    exe_user = models.CharField(max_length=16, verbose_name="执行用户")
    iphost = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    task_status = models.SmallIntegerField(verbose_name="任务状态")   # 0：失败  1：成功  2：等待  3：执行中
    note = models.TextField(verbose_name="备注")
