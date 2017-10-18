# coding: utf8
'''
Created on 2017年8月26日

@author: qiueer
'''

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Task_Def

class TaskDefForm(forms.ModelForm):
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Task_Def
        fields = "__all__"  # 效果与下列的相同
        #fields = ("file", "file_type", "main_script_name", "params", "executor", "task_status", "task_type", "task_perm_status", "func", "create_dt", "update_dt", "create_user")
        #exclude = ['create_dt', "update_dt", "create_user"]
        exclude = ['create_dt', "update_dt", "create_user"]  ## 这两个字段在model中设置为auto_now_add和auto_now，是不可改变的，所以要排除掉
    
        widgets = {
            "params": forms.Textarea(
                attrs={'class': 'select2', "rows": 1}),
            "note": forms.Textarea(
                attrs={"rows": 1}),
            "func": forms.Textarea(
                attrs={"rows": 1}),
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

    
    def clean(self):
        cleaned_data = self.cleaned_data
        tmpfile = cleaned_data.get("file", None)
        remote_file = cleaned_data.get("remote_file", None)
        file_loc = cleaned_data.get("file_loc", None)
        
        max_file_size = 2  # 20M
        if tmpfile and tmpfile.size / 1024 / 1024 > max_file_size:  #文件大小校验
            raise forms.ValidationError(u"文件大小不能大于%sM" % (max_file_size))
        
        if (file_loc == 1 and not tmpfile) or (file_loc == 2 and not remote_file):
                raise forms.ValidationError(u"必须指定本地文件或服务器端文件" )
        return cleaned_data
    
class TaskDefUpdateForm(TaskDefForm):
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Task_Def
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
 

    
    

