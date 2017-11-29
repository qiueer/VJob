# coding: utf8
'''
Created on 2017年8月26日

@author: qiueer
'''

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Comm_Job_Def

class CommJobDefFormNew(forms.ModelForm):
    
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Comm_Job_Def
        fields = "__all__"  # 效果与下列的相同
        #fields = ("file", "file_type", "main_script_name", "params", "executor", "task_status", "task_type", "task_perm_status", "func", "create_dt", "update_dt", "create_user")
        #exclude = ['create_dt', "update_dt", "create_user"]
        exclude = ['create_dt', "update_dt", "create_user", "jobtype", "comm_tasks"]  ## 这两个字段在model中设置为auto_now_add和auto_now，是不可改变的，所以要排除掉
    
        widgets = {
            "func": forms.Textarea(
                attrs={"rows": 1}),
            "note": forms.Textarea(
                attrs={"rows": 1}),
#             'comm_tasks': forms.SelectMultiple(
#                 attrs={'class': 'select2',
#                        'data-placeholder': _('Select task def')}),
        }
        
class CommJobDefForm(forms.ModelForm):
    
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Comm_Job_Def
        fields = "__all__"  # 效果与下列的相同
        #fields = ("file", "file_type", "main_script_name", "params", "executor", "task_status", "task_type", "task_perm_status", "func", "create_dt", "update_dt", "create_user")
        #exclude = ['create_dt', "update_dt", "create_user"]
        exclude = ['create_dt', "update_dt", "create_user", "jobtype"]  ## 这两个字段在model中设置为auto_now_add和auto_now，是不可改变的，所以要排除掉
    
        widgets = {
            "func": forms.Textarea(
                attrs={"rows": 1}),
            "note": forms.Textarea(
                attrs={"rows": 1}),
            'comm_tasks': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select task def')}),
        }
        
#     def _save_m2m(self):
#         super(CommJobDefForm, self)._save_m2m()
#         comm_tasks = self.cleaned_data['comm_tasks']
#         print "-----", comm_tasks
#         self.instance.comm_tasks.clear()
#         self.instance.comm_tasks.add(*tuple(comm_tasks))

#     def save(self, commit=True):
#         comm_jobdef = super(CommJobDefForm, self).save(commit=False)
#         comm_tasks = self.cleaned_data["comm_tasks"]
#         comm_jobdef.save()
#         for ct in comm_tasks:
#             comm_jobdef.comm_tasks.add(ct)
#         return comm_jobdef
    
class CommJobDefUpdateForm(CommJobDefForm):
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Comm_Job_Def
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
 

    
    

