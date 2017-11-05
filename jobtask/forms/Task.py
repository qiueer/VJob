# coding: utf8
'''
Created on 2017年8月26日

@author: qiueer
'''

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Task

class RunTaskForm(forms.ModelForm):
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Task
        fields = ("params", "exe_user", "timeout", "iphosts", "note")
    
        widgets = {
            "params": forms.Textarea(
                attrs={"rows": 1}),
            "note": forms.Textarea(
                attrs={"rows": 2}),
            "timeout": forms.NumberInput(),
            'exe_user': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select task def')}),
            'iphosts': forms.SelectMultiple(
                attrs={'class': 'select2',
                       'data-placeholder': _('Select task type')}),
        }
    
