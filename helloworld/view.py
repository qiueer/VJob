# coding: utf-8
'''
Created on 2017年8月6日

@author: qiueer
'''
#from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.urls import reverse
from django.http.response import HttpResponse

def hello(request):
    #return HttpResponse("Welcome")
    context = {}
    context["hello"] = "Welcome,my friend."
    return render(request, "hello.html", context)

def test_url(request, a, b):
    aa = reverse("abc", args=(a, b))
    print aa
    return HttpResponse("ok")


def home(request):
    #return HttpResponse("Welcome")
    context = {}
    context["title"] = "Welcome,my friend."
    return render(request, "home.html", context)