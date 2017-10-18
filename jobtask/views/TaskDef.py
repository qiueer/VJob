# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.decorators import login_required  
from django.views import View
from django.views import generic

from lib.base.sdate import sdate
from .QBase import QBaseDetailView
from .QBase import QBaseCreateView

from .. import forms
from ..import models
import re

# Create your views here.

class AddView(QBaseCreateView):
    model = models.Task_Def  ## 必填
    form_class  =  forms.TaskDefForm  ## 必填
    template_name = "jobtask/task_def/new.html"  ## 必填
    title = u"创建新任务"
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        now  = sdate().datetime_human()
        update_or_add_fds = {
            "create_dt": now,
            "update_dt": now,
            "create_user": self.request.user.username or 'Admin',
        }
        for (k, v) in update_or_add_fds.iteritems():
            setattr(obj, k, v)
        #return super(QBaseCreateView, self).form_valid(form)
        return QBaseCreateView.form_valid(self, form)

    
##用于更新、删除，继承于UpdateView
class DetailView(QBaseDetailView):
    model = models.Task_Def
    template_name = "jobtask/task_def/detail.html" 
    list_url = reverse_lazy("jobtask:taskdef-list") ## 必填
    form_class  =  forms.TaskDefUpdateForm  ## 必填
    title = u"任务定义详情"
    
    ## form校验通过，修改前更新
    def form_valid(self, form):
        obj = form.save(commit=False)
        now  = sdate().datetime_human()
        update_or_add_fds = {
            "update_dt": now,
        }
        for (k, v) in update_or_add_fds.iteritems():
            setattr(obj, k, v)
        #return super(QBaseDetailView, self).form_valid(form)
        return QBaseDetailView.form_valid(self, form)
    
class ListView(generic.ListView):
    model = models.Task_Def
    template_name = 'jobtask/task_def/list.html'  
    context_object_name = 'dataset'  
    paginate_by = 5 #加上这句就自动开启了分页功能
    allow_empty_first_page = True
    
    class Meta:
        ordering = ['-id']

    def get_querystr_without_page(self):
        query_string_all =  self.request.META.get("QUERY_STRING")
        querystr_widthout_page = re.sub(r"page=\d+", "", query_string_all)
        if querystr_widthout_page.startswith("&") or querystr_widthout_page.endswith("&"):
            querystr_widthout_page = querystr_widthout_page.strip("&")
        return querystr_widthout_page
    
    def get_queryset(self):  
        #cid = self.kwargs.get('cid','')  
        #articles_list = models.Task_Def.objects.filter(category=cid).order_by('-view_times').defer('text')  
        #taskdef_list = models.Task_Def.objects.all()
        fieldmap = {
            "task_status": "task_status",
            "task_type": "task_type",
            "task_perm": "task_perm_status",
            "file_type": "file_type",
        }
        querydict = self.request.GET
        condition = {}
        for (k,vs) in dict(querydict).items():
            if k in fieldmap:
                new_k = fieldmap[k]
                if vs[0]: condition[new_k] = vs[0]
        
        user_open = self.kwargs.get("user-open", False)
        if user_open == True:
            condition["create_user"] = self.request.user.username
        dataset = self.model.objects.filter(**condition).order_by("-create_dt")
        return dataset  
  
    def get_context_data(self,**kwargs):  

        context  = super(ListView,self).get_context_data(**kwargs)
        context["title"] = u"任务列表" if self.kwargs.get("user-open", False) == False else u"我的任务定义列表"
        context["querystr"] = self.get_querystr_without_page()
        getmap = self.request.GET
        for (k,vs) in dict(getmap).items():
            if k == "page": continue  #排除分页参数
            for v in vs: # 有相同的参数
                context[k] = v
        return context
