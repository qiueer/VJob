# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse_lazy
from django.template import loader, Context

from django.contrib.auth.decorators import login_required  
from django.views import View
from django.views import generic

from lib.base.sdate import sdate

from .. import forms
from ..import models
import re
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone



class DetailView(generic.View):
    http_method_names = ["get", "post"]
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("Not Allow")
    
    def get(self, request, *args, **kwargs):
        oid = kwargs.get("pk", None)
        taskid = kwargs.get("taskid", None)
        tpl_name = "jobtask/task/detail.html"
        context = locals()
        context["oid"] = oid
        context["taskid"] = taskid
        context["title"] = u"任务详情"
        return render_to_response(tpl_name, context)
    
    def post(self, request, *args, **kwargs):
        try:
            oid = kwargs.get("pk", None)
            taskid = kwargs.get("taskid", None)
            tpl_name = "jobtask/task/ajax_detail.html"
            context = locals()
            obj = get_object_or_404(models.Task, id=oid)
            context["object"] = obj
            t = loader.get_template(tpl_name)
            data = {"html": t.render(context), "msg": "ok" if obj.task_status==1 else "nook"}
            return JsonResponse(data)
        except Exception:
            import traceback
            print traceback.format_exc()

class ListView(generic.ListView):
    model = models.Task
    template_name = 'jobtask/task/list.html'  
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


class Run(generic.View):
    http_method_names = ["post"]
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("Not Allow")
    
    def post(self, request, *args, **kwargs):
        try:
            comm_taskdef = get_object_or_404(models.Comm_Task_Def, id=args[0])
            now = timezone.now()
            taskid = sdate().datetime_ex()

            #new job
            task_conf = {
                "taskid": taskid, 
                "create_dt": now, 
                "create_user": request.user.get_username(), 
                "task_status": 2,
                "params": comm_taskdef.params or comm_taskdef.task.params,
                "exe_user": comm_taskdef.exe_user,
                "iphosts": comm_taskdef.iphosts,
                "timeout": comm_taskdef.timeout,
                "fromip": request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", None))
            }
            task = models.Task(**task_conf)
            task.taskdef = comm_taskdef.task
            task.save()
                
            ct = comm_taskdef
            iphosts = re.split("[;|,|\s]+", comm_taskdef.iphosts)
            for iphost in iphosts:
                subtask = {
                    "file_loc": ct.task.file_loc,
                    "file": ct.task.file or ct.task.remote_file,
                    "params": ct.params or ct.task.params,
                    "executor": ct.task.executor,
                    "exe_user": ct.exe_user,
                    "iphost": iphost,
                    "create_dt": timezone.now(),
                    "task_status": 2,
                }
                stask = models.SubTask(**subtask)
                stask.task = task
                stask.save()
    
            newurl = reverse_lazy("jobtask:task-detail", kwargs={'pk': task.id, "taskid": taskid})
            data = {"taskid": taskid, "msg":"success", "code": 0, "url": newurl} ## 必填}
            return JsonResponse(data)
        except Exception:
            import traceback
            data = {"taskid": "", "msg": traceback.format_exc(), "code": 1}
            return JsonResponse(data)
        
class RunTask(generic.View):
    http_method_names = ["post"]
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("Not Allow")
    
    def post(self, request, *args, **kwargs):
        try:
            request.POST.get("")
            taskdef = get_object_or_404(models.Task_Def, id=args[0])
            params = request.POST.get("params", None)
            exe_user = request.POST.get("exe_user",None)
            iphosts = request.POST.get("iphosts",None)
            timeout = request.POST.get("timeout", None)
            note = request.POST.get("note",None)
            
            if None in [iphosts, timeout, note]:
                data = {"taskid": "", "msg": "必填项不能为空", "code": 1}
                return JsonResponse(data)
            
            now = timezone.now()
            taskid = sdate().datetime_ex()
            #new job
            task_new = {
                "taskid": taskid,
                "params": params if params else taskdef.params,
                "iphosts": iphosts,
                "timeout": int(timeout),
                "create_dt": now, 
                "create_user": self.request.user.get_username(), 
                "task_status": 2,
                "note": note,
            }
            task = models.Task(**task_new)
            task.taskdef = taskdef
            task.save()

            iphosts = re.split("[;|,|\s]+", iphosts)
            for iphost in iphosts:
                subtask = {
                    "file_loc": taskdef.file_loc,
                    "file": taskdef.file or taskdef.remote_file,
                    "main_script_name": taskdef.main_script_name,
                    "params": params or taskdef.params,
                    "executor": taskdef.executor,
                    "exe_user": exe_user,
                    "iphost": iphost,
                    "create_dt": timezone.now(),
                    "task_status": 2,
                }
                m_subtask = models.SubTask(**subtask)
                m_subtask.task = task
                m_subtask.save()
    
            newurl = reverse_lazy("jobtask:task-detail", kwargs={'pk': task.id, "taskid": taskid})
            data = {"taskid": taskid, "msg":"success", "code": 0, "url": newurl} ## 必填}
            return JsonResponse(data)
        except Exception:
            import traceback
            tb = traceback.format_exc()
            print tb
            data = {"taskid": "", "msg": tb, "code": 1}
            return JsonResponse(data)