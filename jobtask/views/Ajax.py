# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http import JsonResponse
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
    task_status_map = [("", "请选择..."), ("1", "停用"),("2", "启用")]
    data = {"dataset": get_data_list(task_status_map)}
    return JsonResponse(data, safe=True)

@csrf_exempt
def TaskType(request):
    task_type_map = [("", "请选择..."), (1, "系统任务"),(2, "普通任务")]
    data = {"dataset": get_data_list(task_type_map)}
    return JsonResponse(data, safe=True)

@csrf_exempt
def TaskPerm(request):
    task_perm_status_map = [("", "请选择..."), (1, "独享"),(2, "共享")]
    data = {"dataset": get_data_list(task_perm_status_map)}
    return JsonResponse(data, safe=True)

@csrf_exempt
def FileType(request):
    file_type_map = [("", "请选择..."),  (1, "脚本"),(2, "脚本包")]
    data = {"dataset": get_data_list(file_type_map)}
    return JsonResponse(data, safe=True)

@csrf_exempt
def FileLocation(request):
    file_loc_choice = [("", "请选择..."),  (1, "本地"),(2, "服务器")]
    data = {"dataset": get_data_list(file_loc_choice)}
    return JsonResponse(data, safe=True)


@csrf_exempt
def IpList(request):
    queryset = models.SaltMinion.objects.all()
    dataset = []
    #dataset.append({"key":"", "value":"请选择..."})
    for item in queryset:
        dataset.append({"key":item.ip, "value":item.ip})
    data = {"dataset": dataset}
    return JsonResponse(data, safe=True)