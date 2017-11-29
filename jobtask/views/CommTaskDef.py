# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.decorators import login_required  
from django.views import View
from django.views import generic
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone

from lib.base.sdate import sdate
from .QBase import QBaseDetailView
from .QBase import QBaseCreateView

from .. import forms
from .. import models
import re

# Create your views here.

class AddView(QBaseCreateView):
    model = models.Comm_Task_Def  ## 必填
    form_class  =   forms.CommTaskDefForm## 必填
    template_name = "jobtask/comm_task_def/new.html"  ## 必填
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
        obj.iphosts = ";".join(self.request.POST.getlist("iphosts",[]))
        #return super(QBaseCreateView, self).form_valid(form)
        return QBaseCreateView.form_valid(self, form)

##用于更新、删除，继承于UpdateView
class DetailView(QBaseDetailView):
    model = models.Comm_Task_Def
    template_name = "jobtask/comm_task_def/detail.html" 
    list_url = reverse_lazy("jobtask:comm_taskdef-list") ## 必填
    form_class  =  forms.CommTaskDefForm  ## 必填
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
        # select2
        obj.iphosts = ";".join(self.request.POST.getlist("iphosts",[]))
        #return super(QBaseDetailView, self).form_valid(form)
        return QBaseDetailView.form_valid(self, form)
    
# ##用于更新、删除，继承于UpdateView
# class DetailViewForModal(QBaseDetailView):
#     model = models.Comm_Task_Def
#     template_name = "jobtask/modal/comm_taskdef_detail.html" 
#     list_url = reverse_lazy("jobtask:comm_taskdef-list") ## 必填
#     form_class  =  forms.CommTaskDefForm  ## 必填
#     title = u"任务定义详情"

##用于更新、删除，继承于UpdateView
class DetailViewForModal(generic.DetailView):
    model = models.Comm_Task_Def
    template_name = "jobtask/modal/comm_taskdef_detail.html" 

class ListView(generic.ListView):
    model = models.Comm_Task_Def
    template_name = 'jobtask/comm_task_def/list.html'  
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
        
        ## 这里判断是否是个人的常规任务
        user_open = self.kwargs.get("user-open", False)
        if user_open == True:
            condition["create_user"] = self.request.user.username
        dataset = self.model.objects.filter(**condition).order_by("-id")
        return dataset  
  
    def get_context_data(self,**kwargs):  
        context  = super(ListView,self).get_context_data(**kwargs)
        context["title"] = u"任务列表"
        context["querystr"] = self.get_querystr_without_page()
        getmap = self.request.GET
        for (k,vs) in dict(getmap).items():
            if k == "page": continue  #排除分页参数
            for v in vs: # 有相同的参数
                context[k] = v
        return context
    
    
class ListTask(generic.ListView):
    model = models.Comm_Task_Def
    template_name = 'jobtask/comm_task_def/listtask.html'  
    context_object_name = 'dataset'  
    paginate_by = 6 #加上这句就自动开启了分页功能
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
        
        ## 这里判断是否是个人的常规任务
        user_open = self.kwargs.get("user-open", False)
        if user_open == True:
            condition["create_user"] = self.request.user.username
            
        tasks = querydict.get("tasks", None)
        if tasks:
            taskids = [int(tid) for tid in str(tasks).strip("|").split("|")]
            dataset = self.model.objects.filter(**condition).exclude(id__in=taskids).order_by("-id")
            print dataset
            return dataset  
        dataset = self.model.objects.filter(**condition).order_by("-id")
        return dataset  
  
    def get_context_data(self,**kwargs):  
        context  = super(ListTask,self).get_context_data(**kwargs)
        context["title"] = u"任务列表"
        context["querystr"] = ""  #self.get_querystr_without_page()
        context["pagesize"] = self.paginate_by
        getmap = self.request.GET
        for (k,vs) in dict(getmap).items():
            if k == "page": continue  #排除分页参数
            for v in vs: # 有相同的参数
                context[k] = v
        return context