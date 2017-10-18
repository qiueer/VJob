# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render_to_response

from ..models import Book

from django.http.response import HttpResponse

# Create your views here.

def show(request):
    b = Book.objects.get(id=1)
    print str(b),b.title
    return HttpResponse("OK")
