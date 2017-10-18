# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import  HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.shortcuts import render_to_response, render
from django.views.decorators.cache import cache_page

from . import forms
from datetime import date
import datetime

# Create your views here.

#@cache_page(5 * 1, key_prefix="site1")
def display_meta(request):
    infos = request.META.items()
    infos.sort()
    html = []
    for k,v in infos:
        html.append("<tr><td>{0}</td><td>{1}</td></tr>".format(k ,v))

    return HttpResponse("<table>%s</table>" % ("\n".join(html)))

@cache_page(60 * 1, key_prefix="site1")  ## 页面缓存
def display_meta_by_tpl(request):
    return render_to_response("book/display_request_meta.html", {"items": request.META.items()})

def author_form(request):
    af = None
    if request.method == "POST":
        af = forms.AuthorForm(request.POST)
        if af.is_valid():
            cd = af.cleaned_data
            (name, email, age ) = (cd["name"], cd["email"], cd["age"])
            print (name, email, age ) 
            return HttpResponseRedirect("/thanks/")
    else:
        af = forms.AuthorForm()

    context = locals()
    context["form"] = af
    return render(request, "book/author_form.html", context)  ## 为让csrf生效，需要使用render函数，而不能使用render_to_response
    #return render_to_response("book/author_form.html", context)
    
