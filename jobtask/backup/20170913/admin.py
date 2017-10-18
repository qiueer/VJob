# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from jobtask.models import Res_Control_Conf
from jobtask.models import Task_Def
from jobtask.models import Task
from jobtask.models import Comm_Job_Def
from jobtask.models import Comm_Task_Def
from jobtask.models import Job

admin.site.register(Res_Control_Conf)
admin.site.register(Task_Def)
admin.site.register(Task)
admin.site.register(Comm_Job_Def)
admin.site.register(Comm_Task_Def)
admin.site.register(Job)

# Register your models here.
