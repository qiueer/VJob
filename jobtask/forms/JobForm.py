# coding: utf8
'''
Created on 2017年8月26日

@author: qiueer
'''

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Job

class JobForm(forms.ModelForm):
    
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Job
        fields = "__all__"  # 效果与下列的相同
        #fields = ("file", "file_type", "main_script_name", "params", "executor", "task_status", "task_type", "task_perm_status", "func", "create_dt", "update_dt", "create_user")
        #exclude = ['create_dt', "update_dt", "create_user"]
        exclude = ['create_dt', "update_dt", "create_user"]  ## 这两个字段在model中设置为auto_now_add和auto_now，是不可改变的，所以要排除掉