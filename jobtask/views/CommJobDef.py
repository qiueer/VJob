# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.decorators import login_required  
from django.views import View
from django.views import generic
from django.shortcuts import get_object_or_404, render_to_response

from django.http import JsonResponse
from django.http import HttpResponse

from lib.base.sdate import sdate
from .QBase import QBaseDetailView
from .QBase import QBaseCreateView

from .. import forms
from .. import models
import re
from jobtask.views import CommTaskDef
from jobtask.views.CommJobDef2 import DetailView

# Create your views here.

class AddView(QBaseCreateView):
    model = models.Comm_Job_Def  ## 必填
    form_class  =   forms.CommJobDefFormNew## 必填
    template_name = "jobtask/comm_job_def/new.html"  ## 必填
    title = u"创建新作业"
    
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
        #obj.iphosts = ";".join(self.request.POST.getlist("iphosts",[]))
        #return super(QBaseCreateView, self).form_valid(form)
        #print self.request.POST.getlist("comm_tasks")
        
        obj.save()
        #comm_tasks = form.cleaned_data["comm_tasks"]
        tasks = self.request.POST.get("tasks", None)
        if not tasks:
            return self.ret_err_msg("tasks", "任务", "任务不能为空")
        taskids = [int(tid) for tid in str(tasks).strip("|").split("|")]

        #print tasks, taskids
        for tid in taskids:
            ct = models.Comm_Task_Def.objects.get(id=tid)
            models.CommJobTaskConfig.objects.create(comm_job_id=obj.id, comm_task_id=ct.id)
            #obj.comm_tasks.add(ct)
        return QBaseCreateView.form_valid(self, form)
    
##用于更新、删除，继承于UpdateView
class DetailView(QBaseDetailView):
    model = models.Comm_Job_Def
    template_name = "jobtask/comm_job_def/detail.html" 
    list_url = reverse_lazy("jobtask:comm_jobdef-list") ## 必填
    form_class  =  forms.CommJobDefFormNew  ## 必填
    title = u"作业定义详情"
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        jt_config = models.CommJobTaskConfig.objects.filter(comm_job_id=pk)
        context["jobtask_config"] = jt_config
        return context
    
    ## form校验通过，修改前更新
    def form_valid(self, form):
        obj = form.save(commit=False)
        now  = sdate().datetime_human()
        update_or_add_fds = {
            "update_dt": now,
        }
        for (k, v) in update_or_add_fds.iteritems():
            setattr(obj, k, v)
        obj.save()
        
        tasks = self.request.POST.get("tasks", None)
        if not tasks:
            return self.ret_err_msg("tasks", "任务", "任务不能为空")
        taskids = [int(tid) for tid in str(tasks).strip("|").split("|")]

        models.CommJobTaskConfig.objects.filter(comm_job_id=obj.id).delete()
            
        for tid in taskids: ## 顺序新增
            ct = models.Comm_Task_Def.objects.get(id=tid)
            models.CommJobTaskConfig.objects.create(comm_job_id=obj.id, comm_task_id=ct.id)
            #obj.comm_tasks.add(ct)
        return QBaseDetailView.form_valid(self, form)

class ListView(generic.ListView):
    model = models.Comm_Job_Def
    template_name = 'jobtask/comm_job_def/list.html'  
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

        ## 这里判断是否是个人的常规作业
        user_open = self.kwargs.get("user-open", False)
        if user_open == True:
            condition["create_user"] = self.request.user.username
        dataset = self.model.objects.filter(**condition).order_by("-id")
        return dataset  
  
    def get_context_data(self,**kwargs):  
        context  = super(ListView,self).get_context_data(**kwargs)
        context["title"] = u"作业列表"
        context["querystr"] = self.get_querystr_without_page()
        getmap = self.request.GET
        for (k,vs) in dict(getmap).items():
            if k == "page": continue  #排除分页参数
            for v in vs: # 有相同的参数
                context[k] = v
        return context

class DetailViewForModal(generic.DetailView):
    model = models.Comm_Job_Def
    template_name = "jobtask/modal/comm_jobdef_detail.html" 
