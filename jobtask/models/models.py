# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


## 资源控制配置表
class SaltMinion(models.Model):
    ip = models.CharField(max_length=32, verbose_name="IP")
    saltkey = models.CharField(max_length=64, verbose_name="SaltKey")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(blank=True, null=True, verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    note = models.TextField(verbose_name="备注")
    
    class Meta(object):
        db_table = "saltminion"

    def __unicode__(self):
        return "%s"  % self.ip
    
## 资源控制配置表
class Res_Control_Conf(models.Model):
    mem = models.IntegerField(verbose_name="内存要求(M)")
    mem_percent = models.IntegerField(verbose_name="内存要求(%)")
    sys_load_1 = models.FloatField(verbose_name="系统负载要求(1m)")
    sys_load_5 = models.FloatField(verbose_name="系统负载要求(5m)")
    sys_load_15 = models.FloatField(verbose_name="系统负载要求(15m)")

    class Meta(object):
        db_table = "res_control_conf"
        
    def __unicode__(self):
        return "%s"  % self.mem

## 任务定义表
class Task_Def(models.Model):
    ## for select fields
    file_loc = models.SmallIntegerField(null=False, blank=True, verbose_name=u"文件位置")
    file = models.FileField(upload_to="upload/%Y/%m/%d", blank=True, null=True, verbose_name="本地文件")  #文件
    remote_file = models.CharField(null=True, blank=True, max_length=255, verbose_name=u"服务器端文件")
    #filepath = models.CharField(max_length=255, verbose_name="文件路径")  #文件
    file_type = models.SmallIntegerField(verbose_name="文件类型")  # 脚本或脚本包
    main_script_name = models.CharField(max_length=64, verbose_name="主执行程序")
    #path = models.CharField(max_length=255, verbose_name="文件路径")
    params = models.TextField(verbose_name="参数")
    executor = models.CharField(max_length=16, verbose_name="解析器")
    func = models.TextField(verbose_name="功能说明")
    task_status = models.SmallIntegerField(verbose_name="任务状态")
    task_type = models.SmallIntegerField(verbose_name="任务类型")
    task_perm_status = models.SmallIntegerField(verbose_name="任务权限状态")
    res_ctl_conf =  models.ForeignKey(Res_Control_Conf, verbose_name="主机资源控制", null=True, on_delete=models.SET_NULL) 
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(blank=True, null=True, verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    note = models.TextField(verbose_name="备注")

    class Meta(object):
        db_table = "task_def"
        
    def __unicode__(self):
        return "%s - by %s"  % (self.func, self.create_user)
    
## 常规任务表，已配置好
class Comm_Task_Def(models.Model):
    task = models.ForeignKey(Task_Def, verbose_name="选择已定义任务", related_name="comm_task_defs")
    tasktype = models.IntegerField(default=2, verbose_name="任务类型")  # 取值[1,2], 1后台自动生成，2从前端配置生成
    params = models.TextField(blank=True, null=True, verbose_name="参数")
    iphosts = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    exe_user = models.CharField(max_length=64, verbose_name="执行用户") # 在远程主机上执行脚本或任务，主机上的用户
    timeout = models.IntegerField(verbose_name="超时时间")
    func = models.TextField(verbose_name="功能说明")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    note = models.TextField(verbose_name="备注") # 在远程主机上执行脚本或任务，主机上的用户
    
    class Meta(object):
        db_table = "comm_task_def"
        
    def __unicode__(self):
        return "%s"  % self.func
    
class JobStatus(models.Model):
    jobstatus = models.CharField(max_length=32, verbose_name="作业状态")
    jobstatus_cn = models.CharField(max_length=32, verbose_name="作业状态(CN)")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    update_dt = models.DateTimeField(null=True, blank=True, verbose_name="更新时间")
    note = models.TextField(null=True, blank=True, verbose_name="备注")
    
    class Meta(object):
        db_table = "job_status"
        
    def __unicode__(self):
        return "%s "  % (self.jobstatus_cn)
    
    def __str__(self):
        return "%s "  % (self.jobstatus_cn)
    
class JobType(models.Model):
    jobtype = models.CharField(max_length=32, verbose_name="作业类型")
    jobtype_cn = models.CharField(max_length=32, verbose_name="作业类型(CN)")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    update_dt = models.DateTimeField(null=True, blank=True, verbose_name="更新时间")
    note = models.TextField(null=True, blank=True, verbose_name="备注")
    
    def __unicode__(self):
        return "%s"  % (self.jobtype_cn)
    
    def __str__(self):
        return "%s"  % (self.jobtype_cn)
    
    class Meta(object):
        db_table = "job_type"
    
class JobClass(models.Model):
    jobclass = models.CharField(max_length=32, verbose_name="作业分类")
    jobclass_cn = models.CharField(max_length=32, verbose_name="作业分类(CN)")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")
    update_dt = models.DateTimeField(null=True, blank=True, verbose_name="更新时间")
    note = models.TextField(null=True, blank=True, verbose_name="备注")
    
    def __unicode__(self):
        return "%s"  % (self.jobclass_cn)
    
    def __str__(self):
        return "%s "  % (self.jobclass_cn)
    
    class Meta(object):
        db_table = "job_class"
    
## 常规作业表，已配置好
class Comm_Job_Def(models.Model):
    comm_tasks = models.ManyToManyField(Comm_Task_Def, verbose_name="任务列表", through="CommJobTaskConfig", through_fields=("comm_job", "comm_task"))
    job_status = models.ForeignKey(JobStatus, default=None, verbose_name="作业状态")  # 0：停用；1：启用
    jobtype = models.IntegerField(default=2, verbose_name="任务类型")  # 取值[1,2], 1后台自动生成，2从前端配置生成
    job_class = models.ForeignKey(JobClass, default=None, verbose_name="作业分类")  # 0：独有不公开  1：所有人可读
    func = models.TextField(verbose_name="功能说明")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    note = models.TextField(verbose_name="备注")
    
    class Meta(object):
        db_table = "comm_job_def"
        
class CommJobTaskConfig(models.Model):
    comm_job = models.ForeignKey(Comm_Job_Def, on_delete=models.CASCADE)
    comm_task = models.ForeignKey(Comm_Task_Def, on_delete=models.CASCADE)
    create_dt = models.DateTimeField(auto_now_add=True)
    
    class Meta(object):
        db_table = "comm_job_task_config"
        
# 创建作业
# 创建任务

# 作业表
class Job(models.Model):
    jobdef = models.ForeignKey(Comm_Job_Def, default=None, verbose_name="作业")
    jobid = models.CharField(max_length=64, verbose_name="作业单号") 
    job_class = models.ForeignKey(JobClass, default=None, verbose_name="作业分类")  # 0：独有不公开  1：所有人可读
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    create_user = models.CharField(null=True, max_length=64, verbose_name="创建用户")
    job_status =  models.SmallIntegerField(verbose_name="作业状态")   # 0：失败  1：成功  2：等待  3：执行中
    
    class Meta:
        db_table = "job"
        indexes = [
            models.Index(fields=['jobid'], name='jobid_idx'),
        ]

class Job_Task(models.Model):
    job = models.ForeignKey(Job, default=None, verbose_name="作业", related_name="job_tasks")
    comm_task = models.ForeignKey(Comm_Task_Def, default=None, verbose_name="任务定义", related_name="comm_tasks")
    file_loc = models.SmallIntegerField(null=False, blank=False, default=1, verbose_name=u"文件位置")  ## 1,本地；2,远程服务器端
    file = models.CharField(null=True, blank=True, max_length=255, verbose_name=u"文件路径")
    main_script_name = models.CharField(max_length=64, default="", verbose_name="主执行程序")
    params = models.TextField(verbose_name="参数")
    iphosts = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    exe_user = models.CharField(max_length=64, verbose_name="执行用户") # 在远程主机上执行脚本或任务，主机上的用户
    timeout = models.IntegerField(verbose_name="超时时间")
    fromip = models.CharField(max_length=16, verbose_name="任务状态")
    create_user = models.CharField(max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    job_task_status = models.SmallIntegerField(blank=True, null=True, verbose_name="任务状态")   # 0：失败  1：成功  2：等待  3：执行中
    note = models.TextField(verbose_name="备注")
    
    class Meta(object):
        db_table = "job_task"

class Job_SubTask(models.Model):
    jobtask = models.ForeignKey(Job_Task, default=None, verbose_name="作业任务", related_name="job_sub_tasks")
    file_loc = models.SmallIntegerField(null=False, blank=True, default=1, verbose_name=u"文件位置")  ## 1,本地；2,远程服务器端
    file = models.CharField(null=True, blank=True, max_length=255, verbose_name=u"文件路径")
    main_script_name = models.CharField(max_length=64, default="", verbose_name="主执行程序")
    params = models.TextField(verbose_name="参数")
    executor = models.CharField(max_length=16, verbose_name="解析器")
    exe_user = models.CharField(max_length=16, verbose_name="执行用户")
    iphost = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    task_status = models.SmallIntegerField(blank=True, null=True, verbose_name="任务状态")   # 0：失败  1：成功  2：等待  3：执行中
    retcode = models.SmallIntegerField(null=True, blank=True, verbose_name="执行返回码")
    stdout = models.TextField(null=True, blank=True, verbose_name="标准输出")
    stderr = models.TextField(null=True, blank=True, verbose_name="标准错误输出")
    note = models.TextField(verbose_name="备注")
    
    class Meta(object):
        db_table = "job_subtask"
    
### 另外一个通道
class Task(models.Model):
    taskdef = models.ForeignKey(Task_Def, verbose_name="选择已定义任务", related_name="tasks")
    taskid = models.CharField(null=True, max_length=64, verbose_name="任务号") 
    exe_user = models.CharField(max_length=64, verbose_name="执行用户") # 在远程主机上执行脚本或任务，主机上的用户
    params = models.TextField(verbose_name="参数")
    iphosts = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    timeout = models.IntegerField(default=0, verbose_name="超时时间")
    fromip = models.CharField(blank=True, null=True, max_length=16, verbose_name="任务状态")
    task_status = models.SmallIntegerField(blank=True, null=True, verbose_name="任务状态")   # 0：失败  1：成功  2：等待  3：执行中
    create_user = models.CharField(blank=True, null=True, max_length=64, verbose_name="创建用户")
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    note = models.TextField(verbose_name="备注")
    
    class Meta(object):
        db_table = "task"

class SubTask(models.Model):
    task = models.ForeignKey(Task, default=None, verbose_name="作业任务", related_name="subtasks")
    file_loc = models.SmallIntegerField(null=False, blank=True, default=1, verbose_name=u"文件位置")  ## 1,本地；2,远程服务器端
    file = models.CharField(null=True, blank=True, max_length=255, verbose_name=u"文件路径")
    main_script_name = models.CharField(max_length=64, default="", verbose_name="主执行程序")
    params = models.TextField(verbose_name="参数")
    executor = models.CharField(max_length=16, verbose_name="解析器")
    exe_user = models.CharField(max_length=16, verbose_name="执行用户")
    iphost = models.TextField(verbose_name="IP或主机名") # 在远程主机上执行脚本或任务，主机上的用户
    create_dt = models.DateTimeField(verbose_name="创建时间")
    update_dt = models.DateTimeField(blank=True, null=True, verbose_name="更新时间")
    task_status = models.SmallIntegerField(blank=True, null=True, verbose_name="任务状态")   # 0：失败  1：成功  2：等待  3：执行中
    retcode = models.SmallIntegerField(null=True, blank=True, verbose_name="执行返回码")
    stdout = models.TextField(null=True, blank=True, verbose_name="标准输出")
    stderr = models.TextField(null=True, blank=True, verbose_name="标准错误输出")
    note = models.TextField(verbose_name="备注")
    
    class Meta(object):
        db_table = "subtask"