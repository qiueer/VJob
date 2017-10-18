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
from pip._vendor.requests.api import delete

# Create your views here.

class AddView(generic.CreateView):
    model = models.Task_Def  ## 必填
    form_class  =  forms.TaskDefForm  ## 必填
    template_name = "jobtask/taskdef_new.html"  ## 必填
    success_url = reverse_lazy("jobtask:taskdef-list")  ## 可选，其实没用
    
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

    ## 验证不通过时
    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        ## 只存储一个error
        respdata = {}
        fields = self.model._meta.fields
        for (k, v) in form.errors.iteritems():
            if respdata: break
            for fd in fields:
                if respdata: break
                if fd.name == k:
                    respdata = {"field": k, "verbose_name": fd.verbose_name, "errmsg": ";".join(v) }

        return HttpResponse(JsonResponse(respdata), content_type="application/json")  

    def form_valid(self, form):
        self.taskdef = taskdef = form.save(commit=False)
        now  = sdate().datetime_human()
        taskdef.create_user = self.request.user.username or 'Admin'
        taskdef.create_dt = now
        taskdef.update_dt = now
        taskdef.save()
        result =  super(AddView, self).form_valid(form) # django.http.response.HttpResponseRedirect
        #return result
        respdata = {"id": taskdef.id, "msg":"success"}
        # 返回JSON，可以在同一个页面多次添加
        return HttpResponse(JsonResponse(respdata), content_type="application/json")  

    def get_context_data(self,**kwargs):  
        context  = super(AddView,self).get_context_data(**kwargs)
        context["title"] = u"任务定义"
        context["action"] = self.request.META.get("PATH_INFO","")
        context["success_url"] = self.success_url
        return context
    
class DetailView_old(generic.DetailView):
#class DetailView(generic.UpdateView):
    model = models.Task_Def
    template_name = "jobtask/taskdef_detail_old.html"
    def get_context_data(self, **kwargs):
            context = super(DetailView_old, self).get_context_data(**kwargs)
            context['title'] = u"任务详情"
            #print "*****", self.kwargs  # 输入的参数，可以由self.kwargs获取
            excludes = []
            fields = self.model._meta.fields
            params = [f for f in fields if f.name not in excludes]
            for p in params:
                p.attrs = {"required": "true", "abc": 1}
            context["fields"] = params
            return context
    
##用于更新、删除，继承于UpdateView
class DetailView(generic.UpdateView):
    model = models.Task_Def
    template_name = "jobtask/taskdef_detail.html"
    list_url = reverse_lazy("jobtask:taskdef-list",)
    
    form_class  =  forms.TaskDefForm  ## 必填
    respdata = {
            "code": 0,  # 0, success
            "action": "",
            "list_url": list_url, 
            "errmsg": "",
    }
    
    def get_context_data(self, **kwargs):

            context = super(DetailView, self).get_context_data(**kwargs)
            context['title'] = u"任务详情"
            context["action"] = self.request.META.get("PATH_INFO","")  # uri
            #print "*****", self.kwargs  # 输入的参数，可以由self.kwargs获取
            return context
        
    def post(self, request, *args, **kwargs):
        ## delete不需要输入任何数据，pk值可从uri中获取
        ## delete同时也不需要校验
        """
        先执行post方法，然后再到dispatch到form_invalid或form_valid
        """
        action = request.GET.get("_action", None)
        ## 返回默认，继续处理下一步
        if action not in ["delete"]: return generic.UpdateView.post(self, request, *args, **kwargs)
        pk_val = kwargs.get(self.pk_url_kwarg, None)
        obj = self.model.objects.filter(id=pk_val)
        self.respdata.update({"action": action})
        try:
            if "delete"  == action:
                deleted, _rows_count = obj.delete()  ## delete
                self.respdata.update({"code": 0 if deleted > 0 else 1, "errmsg": "delete error"})
                return HttpResponse(JsonResponse(self.respdata), content_type="application/json")  
        except Exception:
            import traceback
            self.respdata.update({"code": 1, "errmsg":traceback.format_exc()})
            return HttpResponse(JsonResponse(self.respdata), content_type="application/json")  
        
    def form_invalid(self, form):
        ## 验证不通过时，返回错误，这里只有update操作才回校验失败
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        ## 只存储一个error
        in_respdata = {}
        fields = self.model._meta.fields
        for (k, v) in form.errors.iteritems():
            if in_respdata: break
            for fd in fields:
                if in_respdata: break
                if fd.name == k:
                    in_respdata = {"errmsg": fd.verbose_name+":"+";".join(v), "code": 1}

        self.respdata.update(in_respdata)
        return HttpResponse(JsonResponse(self.respdata), content_type="application/json")  

    def form_valid(self, form):
        ## form_valid验证通过后，这里才能做更新
        self.taskdef = taskdef = form.save(commit=False)
        now  = sdate().datetime_human()
        taskdef.create_user = self.request.user.username or 'Admin'
        taskdef.create_dt = now
        taskdef.update_dt = now
        taskdef.save()
        #print self.request.META.get("PATH_INFO",None)
        respdata = {"code": 0, "errmsg":"success", "action": self.request.GET.get("_action", "None")}
        self.respdata.update(respdata)
        # 返回JSON，可以在同一个页面多次添加
        return HttpResponse(JsonResponse(respdata), content_type="application/json")
        # 默认返回值
        #result =  super(DetailView, self).form_valid(form) # django.http.response.HttpResponseRedirect
        
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
