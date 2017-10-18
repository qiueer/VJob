# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import  HttpResponse, HttpResponseRedirect
from django.http import JsonResponse


from django.shortcuts import render_to_response, render
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.decorators import login_required  
from django.views import View

from django.views import generic

from lib.base.sdate import sdate

from .. import forms
from ..import models
import re

# Create your views here.

class AddView(generic.CreateView):
    #model = models.Task_Def
    form_class  =  forms.TaskDefForm
    template_name = "jobtask/taskdef_new.html"
    success_url = reverse_lazy("jobtask:taskdef-list")
    
    ## for get method
#     def get_form_kwargs(self):
#         now = sdate().datetime_human()
#         kwargs = super(AddView, self).get_form_kwargs()
# #         kwargs["create_dt"] = now
# #         kwargs["update_dt"] = now
# #         kwargs["create_user"] = self.request.user.get_username()
#         print "2222222",kwargs
#         return kwargs  

    def get_initial(self):
        default_init = {}
        now = sdate().datetime_human()
        default_init['create_dt'] = now
        default_init['update_dt'] = now
        return default_init

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST["create_user"] = self.request.user.get_username() ## 添加当前用户
        return super(AddView, self).post(request, **kwargs)

    def form_valid(self, form):
        now  = sdate().datetime_human()
        super(AddView, self).form_valid(form)
        # 这里要加上
        form.instance.create_dt = now
        form.instance.update_dt= now    
        return super(AddView, self).form_valid(form)
     
    def get_context_data(self,**kwargs):  
        context  = super(AddView,self).get_context_data(**kwargs)
        context["title"] = u"任务定义"
        return context
    
class DetailView(generic.DetailView):
#class DetailView(generic.UpdateView):
    model = models.Task_Def
    template_name = "jobtask/taskdef_detail.html"
    def get_context_data(self, **kwargs):
            context = super(DetailView, self).get_context_data(**kwargs)
            context['title'] = u"任务详情"
            #print "*****", self.kwargs  # 输入的参数，可以由self.kwargs获取
            excludes = []
            fields = self.model._meta.fields
            params = [f for f in fields if f.name not in excludes]
            for p in params:
                p.attrs = {"required": "true", "abc": 1}
            context["fields"] = params
            return context
    
class UpdateView(generic.UpdateView):
    model = models.Task_Def
    template_name = "jobtask/taskdef_detail.html"
    def get_context_data(self, **kwargs):
            context = super(DetailView, self).get_context_data(**kwargs)
            context['title'] = u"任务详情"
            #print "*****", self.kwargs  # 输入的参数，可以由self.kwargs获取
            return context
        
class ListView(generic.ListView):
    model = models.Task_Def
    template_name = 'jobtask/taskdef_list.html'  
    context_object_name = 'taskdef_list'  
    paginate_by = 5 #加上这句就自动开启了分页功能
    allow_empty_first_page = True
    
    class Meta:
        ordering = ['-id']

    def get_cleaned_querystr(self):
        getmap = self.request.GET
        ary = list()
        for (k,vs) in dict(getmap).items():
            if k == "page": continue  #排除分页参数
            for v in vs: # 有相同的参数
                ary.append("%s=%s" % (k,v))
        querystr = "&".join(ary)
        return querystr
    
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
        
        taskdef_list = models.Task_Def.objects.filter(**condition)
        return taskdef_list  
  
    def get_context_data(self,**kwargs):  
        context  = super(ListView,self).get_context_data(**kwargs)
#         q = self.request.GET.get("browse", "")
#         context['input'] = q
        context["title"] = u"任务列表"
        context["querystr"] = self.get_cleaned_querystr()
        getmap = self.request.GET
        for (k,vs) in dict(getmap).items():
            if k == "page": continue  #排除分页参数
            for v in vs: # 有相同的参数
                context[k] = v
        return context
    
class ActionView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        obj = {}
        exclude_fields = ["__action" , "csrfmiddlewaretoken" , "create_dt", "update_dt", "create_user"]
        actions = ["clone", "update", "delete"] 
        
        postdic = dict(request.POST)
        action = postdic.get("__action", "None")
        action = str(action[0]).lower()

        print postdic
        for k,vs in postdic.items():
            if k in exclude_fields: continue
            obj[k] = vs[0]

        if action not in actions or "id" not in obj:
            return HttpResponse(status=403)
        
        mdl = models.Task_Def.objects
        resp_data = {"action":action}
        if action == "clone":
            del(obj["id"])
            obj["create_user"] = self.request.user.get_username() 
            crt_obj = mdl.create(**obj)
            new_url = reverse_lazy("jobtask:taskdef-detail", args=(crt_obj.id,))
            resp_data["new_url"] = new_url
            resp_data["id"] = crt_obj.id
        if action == "update":
            obj["update_dt"] = sdate().datetime_human()
            rows = mdl.filter(id=int(obj["id"])).update(**obj)
            resp_data["rows"] = rows
        if action == "delete":
            deleted, _rows_count = mdl.filter(id=int(obj["id"])).delete()
            resp_data["deleted"] = deleted

        return HttpResponse(JsonResponse(resp_data), content_type="application/json")  
