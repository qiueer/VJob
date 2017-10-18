# coding: utf8
'''
Created on 2017年8月26日

@author: qiueer
'''

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Comm_Task_Def
import json

class CommTaskDefForm(forms.ModelForm):
    
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Comm_Task_Def
        fields = "__all__"  # 效果与下列的相同
        #fields = ("file", "file_type", "main_script_name", "params", "executor", "task_status", "task_type", "task_perm_status", "func", "create_dt", "update_dt", "create_user")
        #exclude = ['create_dt', "update_dt", "create_user"]
        exclude = ['create_dt', "update_dt", "create_user", "tasktype"]  ## 这两个字段在model中设置为auto_now_add和auto_now，是不可改变的，所以要排除掉
    
        widgets = {
            "params": forms.Textarea(
                attrs={"rows": 1}),
            "note": forms.Textarea(
                attrs={"rows": 1}),
            "func": forms.Textarea(
                attrs={"rows": 1}),
            'task': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select task def')}),
            'iphosts': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select task type')}),
        }
    
class CommTaskDefUpdateForm(CommTaskDefForm):
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Comm_Task_Def
        fields = "__all__"  # 效果与下列的相同
        #fields = ("file", "file_type", "main_script_name", "params", "executor", "task_status", "task_type", "task_perm_status", "func", "create_dt", "update_dt", "create_user")
        #exclude = ['create_dt', "update_dt", "create_user"]
        #exclude = ["create_user"]  ## 这两个字段在model中设置为auto_now_add和auto_now，是不可改变的，所以要排除掉
    
        widgets = {
            "params": forms.Textarea(
                attrs={'class': 'select2', "rows": 1}),
            "note": forms.Textarea(
                attrs={"rows": 1}),
            "func": forms.Textarea(
                attrs={"rows": 1}),
           "create_dt": forms.TextInput(
               attrs={"readonly": "readonly"}),
           "update_dt": forms.TextInput(
               attrs={"readonly": "readonly"}),
           "create_user": forms.TextInput(
               attrs={"readonly": "readonly"}),
            'file_loc': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select file location')}),
            'file_type': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select file type')}),
            'task_type': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select task type')}),
            'task_status': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select task status')}),
            'task_perm_status': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select perm status')}),
        }
 

    
    

