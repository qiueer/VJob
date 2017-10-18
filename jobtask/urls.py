#coding=utf-8
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


import views

app_name = "jobtask"  # namespace
urlpatterns = [
    ## TaskDef
    #url(r"taskdef/add$", jobtask_views.taskadd, name="taskdef-add"),
    url(r"taskdef/add$", views.TaskDef.AddView.as_view(), name="taskdef-add"),
    url(r'^taskdef/(?P<pk>\d+)$', views.TaskDef.DetailView.as_view(), name='taskdef-detail'), #old
    url(r"^taskdef/list$", views.TaskDef.ListView.as_view(), name="taskdef-list"),
    # ajax
    url(r"^taskdef/status$", views.Ajax.TaskStatus, name="taskdef-status"),
    url(r"^taskdef/type$", views.Ajax.TaskType, name="taskdef-type"),
    url(r"^taskdef/perm$", views.Ajax.TaskPerm, name="taskdef-perm"),
    url(r"^taskdef/filetype$", views.Ajax.FileType, name="taskdef-filetype"),
    url(r"^taskdef/fileloc$", views.Ajax.FileLocation, name="taskdef-filelocation"),
    url(r"^iplist$", views.Ajax.IpList, name="comm-iplist"),
    ## CommTaskDef
    url(r"^comm_taskdef/new$", views.CommTaskDef.AddView.as_view(), name="comm_taskdef-new"),
    url(r"^comm_taskdef/list$", views.CommTaskDef.ListView.as_view(), name="comm_taskdef-list"),
    url(r"^comm_taskdef/(?P<pk>\d+)$", views.CommTaskDef.DetailView.as_view(), name="comm_taskdef-detail"),
    url(r"^comm_taskdef/modal/(?P<pk>\d+)$", views.CommTaskDef.DetailViewForModal.as_view(), name="comm_taskdef-detail_for_modal"),
    ## CommJobDef
    url(r"^comm_jobdef/new$", views.CommJobDef.AddView.as_view(), name="comm_jobdef-new"),
    url(r"^comm_jobdef/list$", views.CommJobDef.ListView.as_view(), name="comm_jobdef-list"),
    url(r"^comm_jobdef/(?P<pk>\d+)$", views.CommJobDef.DetailView.as_view(), name="comm_jobdef-detail"),
    ## Job
    url(r"^job/list$", views.Job.ListView.as_view(), name="job-list"),
    url(r"^job/(?P<pk>\d+)/(?P<jobid>\d+)$", views.Job.DetailView.as_view(), name="job-detail"),
    #url(r"^job/(?P<pk>\d+)$", views.Job.DetailView.as_view(), name="job-detail"),
    url(r"^job/run/(\d+)$", views.Job.RunJob.as_view(), name="job-new"),
    ## JobTask
    url(r"^jobtask/list$", views.JobTask.ListView.as_view(), name="jobtask-list"),
    url(r"^jobtask/(?P<pk>\d+)/(?P<jobid>\d+)/(?P<job_order_id>\d+)$", views.JobTask.DetailView.as_view(), name="jobtask-detail"),
    ## JobSubTask
    url(r"^jobsubtask/list$", views.JobSubTask.ListView.as_view(), name="jobsubtask-list"),
    url(r"^jobsubtask/(?P<pk>\d+)/(?P<taskid>\d+)$", views.JobSubTask.DetailView.as_view(), name="jobsubtask-detail"),
    ## Task
    url(r"^task/list$", views.Task.ListView.as_view(), name="task-list"),
    url(r"^task/(?P<pk>\d+)/(?P<taskid>\d+)$", views.Task.DetailView.as_view(), name="task-detail"),
    url(r"^task/run/(\d+)$", views.Task.Run.as_view(), name="task-run"),
    ## SubTask
    url(r"^subtask/list$", views.SubTask.ListView.as_view(), name="subtask-list"),
    url(r"^subtask/(?P<pk>\d+)/(?P<taskid>\d+)$", views.SubTask.DetailView.as_view(), name="subtask-detail"),
]

## 用户
urlpatterns += [
    ## TaskDef
    url(r"task/def$", views.TaskDef.AddView.as_view(), name="create-my-taskdef"),
    url(r"^task/def/my$", views.TaskDef.ListView.as_view(), {"user-open": True}, name="my-taskdef-list"),
    url(r'^task/def/my/(?P<pk>\d+)$', views.TaskDef.DetailView.as_view(), name='my-taskdef-detail'), #old
]