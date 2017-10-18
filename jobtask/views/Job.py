# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse_lazy
from django.template import loader, Context

from django.contrib.auth.decorators import login_required  
from django.views import View
from django.views import generic

from lib.base.sdate import sdate
from .QBase import QBaseDetailView
from .QBase import QBaseCreateView

from .. import forms
from ..import models
import re
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone

# Create your views here.

##用于更新、删除，继承于UpdateView
# class DetailView(generic.DetailView):
#     model = models.Job
#     template_name = "jobtask/job/detail.html" 

class DetailView(generic.View):
    http_method_names = ["get", "post"]
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("Not Allow")
    
    def get(self, request, *args, **kwargs):
        oid = kwargs.get("pk", None)
        jobid = kwargs.get("jobid", None)
        tpl_name = "jobtask/job/detail.html"
        context = locals()
        context["oid"] = oid
        context["jobid"] = jobid
        context["title"] = u"作业任务详情"
        return render_to_response(tpl_name, context)
    
    def post(self, request, *args, **kwargs):
        try:
            oid = kwargs.get("pk", None)
            jobid = kwargs.get("jobid", None)
            tpl_name = "jobtask/job/ajax_detail.html"
            context = locals()
            obj = get_object_or_404(models.Job, id=oid, jobid=jobid)
            context["object"] = obj
            t = loader.get_template(tpl_name)
            data = {"html": t.render(context), "msg": "ok" if obj.job_status==1 else "nook"}
            return JsonResponse(data)
        except Exception:
            import traceback
            print traceback.format_exc()
            pass

class ListView(generic.ListView):
    model = models.Job
    template_name = 'jobtask/job/list.html'  
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
        
        dataset = self.model.objects.filter(**condition)
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


class RunJob(generic.View):
    http_method_names = ["post"]
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("Not Allow")
    
    def post(self, request, *args, **kwargs):
        try:
            jobdef = get_object_or_404(models.Comm_Job_Def, id=args[0])
            now = timezone.now()
            jobid = sdate().datetime_ex()
            #new job
            job = {
                "jobid": jobid, 
                "create_dt": now, 
                "create_user": self.request.user.get_username(), 
                "job_status": 2,
            }
            job = models.Job(**job)
            job.jobdef = jobdef
            job.job_class = jobdef.job_class
            job.save()
    
            for ct in jobdef.comm_tasks.all():
                jobtask = {
                    "file_loc": ct.task.file_loc,
                    "file": ct.task.file or ct.task.remote_file,
                    "main_script_name": ct.task.main_script_name,
                    "exe_user": ct.exe_user,
                    "params": ct.params,
                    "iphosts": ct.iphosts,
                    "timeout": ct.timeout,
                    "create_user": self.request.user.get_username(),
                    "create_dt": timezone.now(),
                    "job_task_status": 2
                }
                jt = models.Job_Task(**jobtask)
                jt.job = job
                jt.comm_task = ct
                jt.save()
                
                iphosts = re.split("[;|,|\s]+", ct.iphosts)
                for iphost in iphosts:
                    jobsubtask = {
                        "file_loc": ct.task.file_loc,
                        "file": ct.task.file or ct.task.remote_file,
                        "main_script_name": ct.task.main_script_name,
                        "params": ct.params or ct.task.params,
                        "executor": ct.task.executor,
                        "exe_user": ct.exe_user,
                        "iphost": iphost,
                        "create_dt": timezone.now(),
                        "task_status": 2,
                    }
                    jstask = models.Job_SubTask(**jobsubtask)
                    jstask.jobtask = jt
                    jstask.save()
    
            newurl = reverse_lazy("jobtask:job-detail", kwargs={'pk': job.id, "jobid": jobid})
            data = {"jobid": jobid, "msg":"success", "code": 0, "url": newurl} ## 必填}
            return JsonResponse(data)
        except Exception:
            import traceback
            data = {"jobid": "", "msg": traceback.format_exc(), "code": 1}
            return JsonResponse(data)