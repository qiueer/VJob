# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import generic
import re
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class QBaseCreateView(LoginRequiredMixin, generic.CreateView):
    model = None
    form_class  =  None
    template_name = None
    desc = None
    title = None

    def get_context_data(self,**kwargs):
        if None in [self.model, self.template_name, self.form_class]:
            return HttpResponse("ERROR")
        context  = super(QBaseCreateView,self).get_context_data(**kwargs)
        context["title"] = self.title or u"新增"
        context["desc"] = self.desc or u""
        context["action"] = self.request.META.get("PATH_INFO","")
        return context
    
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
                    
        if not respdata:           
            for err in form.non_field_errors():
                respdata = {"errmsg": err,"code": 1}
                break
        return HttpResponse(JsonResponse(respdata), content_type="application/json")  

    def form_valid(self, form):
        self.obj = obj = form.save(commit=False)
        obj.save()
        #result =  super(QBaseCreateView, self).form_valid(form) # django.http.response.HttpResponseRedirect
        #return result
        # 返回JSON，可以在同一个页面多次添加
        respdata = {"id": obj.id, "msg":"success"}
        return HttpResponse(JsonResponse(respdata), content_type="application/json")  

##用于更新、删除，继承于UpdateView
class QBaseDetailView(LoginRequiredMixin, generic.UpdateView):
    model = None
    template_name = None
    list_url = None
    form_class  =  None
    title = None
    respdata = {
            "code": 0,  # 0, success
            "action": "",
            "list_url": "", 
            "errmsg": "",
    }
    
    def after_form_valid(self, **kwargs):
        form = self.get_form()
        obj = form.save(commit=False)
        for (k, v) in dict(kwargs):
            setattr(obj, k, v)
        return obj

    def get_context_data(self, **kwargs):
        if None in [self.model, self.template_name, self.list_url, self.form_class]:
            return HttpResponse("ERROR")
        self.respdata.update({"list_url": self.list_url})
        context = super(QBaseDetailView, self).get_context_data(**kwargs)
        context['title'] = self.title or u"详情"
        context["action"] = self.request.META.get("PATH_INFO","")  # uri, for form
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
         
        if not in_respdata:           
            for err in form.non_field_errors():
                in_respdata = {"errmsg": err,"code": 1}
                break
            
        self.respdata.update(in_respdata)
        return HttpResponse(JsonResponse(self.respdata), content_type="application/json")  

    def form_valid(self, form):
        ## form_valid验证通过后，这里才能做更新
        self.obj = obj = form.save(commit=False)
        obj.save()
        #print self.request.META.get("PATH_INFO",None)
        respdata = {"code": 0, "errmsg":"success", "action": self.request.GET.get("_action", "None")}
        self.respdata.update(respdata)
        # 返回JSON，可以在同一个页面多次添加
        return HttpResponse(JsonResponse(respdata), content_type="application/json")
        # 默认返回值
        #result =  super(DetailView, self).form_valid(form) # django.http.response.HttpResponseRedirect

