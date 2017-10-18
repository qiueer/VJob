# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import JsonResponse

from django.shortcuts import render_to_response, render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy



from lib.base.sdate import sdate

from .. import forms
from ..import models
import re

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def get_data_list(data):
    datalist = []
    for (val, desc) in data:
        datalist.append({"value": val, "key": desc})
    return datalist

@csrf_exempt
def TaskStatus(request):
    task_status_map = [("", "请选择..."), ("0", "停用"),("1", "启用")]
    data = {"dataset": get_data_list(task_status_map)}
    return JsonResponse(data, safe=True)

@csrf_exempt
def TaskType(request):
    task_type_map = [("", "请选择..."), (0, "系统任务"),(1, "普通任务")]
    data = {"dataset": get_data_list(task_type_map)}
    return JsonResponse(data, safe=True)

@csrf_exempt
def TaskPerm(request):
    task_perm_status_map = [("", "请选择..."), (0, "独享"),(1, "共享")]
    data = {"dataset": get_data_list(task_perm_status_map)}
    return JsonResponse(data, safe=True)

@csrf_exempt
def FileType(request):
    file_type_map = [("", "请选择..."),  (0, "脚本"),(1, "脚本包")]
    data = {"dataset": get_data_list(file_type_map)}
    return JsonResponse(data, safe=True)