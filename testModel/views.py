# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

from .models import Test

def testdb(request):
    Test(name='qiueer').save()
    
        # 输出所有数据
    list = Test.objects.all()
    response1 = ""
    for var in list:
        response1 += var.name + "; "
    response = response1
    return HttpResponse(response)