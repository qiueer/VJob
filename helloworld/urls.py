# coding: utf-8
"""helloworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from . import view
from testModel import views
from book.tv import qq
from book import views as book_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello$', view.hello),
    url(r'^qq/$', qq.show ),
    #url(r'^display/$', book_views.display_meta ),
    url(r'^display/$', book_views.display_meta_by_tpl),
    url(r'^book/author_form/$', book_views.author_form),
    url(r"abcd/(\d+)/(\d+)/$", view.test_url, name="abc"),
    url(r"home/$", view.home, name="home"),
    url(r"^jobtask/", include("jobtask.urls", namespace="jobtask")),   # 使用include
]
