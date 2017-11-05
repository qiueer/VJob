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

# Create your views here.

class DetailView(generic.View):
    http_method_names = ["get", "post"]
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("Not Allow")
    
    def get(self, request, *args, **kwargs):
        oid = kwargs.get("pk", None)
        taskid = kwargs.get("taskid", None)
        tpl_name = "jobtask/jobsubtask/detail.html"
        context = locals()
        context["oid"] = oid
        context["taskid"] = taskid
        context["title"] = u"子任务执行详情"
        return render_to_response(tpl_name, context)
    
    def post(self, request, *args, **kwargs):
        try:
            oid = kwargs.get("pk", None)
            taskid = kwargs.get("taskid", None)
            tpl_name = "jobtask/jobsubtask/ajax_detail.html"
            context = locals()
            obj = get_object_or_404(models.Job_SubTask, id=oid)
            context["object"] = obj
            t = loader.get_template(tpl_name)
            data = {"html": t.render(context), "msg": "ok" if obj.task_status==1 else "nook"}
            return JsonResponse(data)
        except Exception:
            import traceback
            print traceback.format_exc()
            pass

class ListView(generic.ListView):
    model = models.Job_SubTask
    template_name = 'jobtask/jobsubtask/list.html'  
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
        context["title"] = u"作业子任务列表"
        context["querystr"] = self.get_querystr_without_page()
        getmap = self.request.GET
        for (k,vs) in dict(getmap).items():
            if k == "page": continue  #排除分页参数
            for v in vs: # 有相同的参数
                context[k] = v
        return context
