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


from jobtask import views as jobtask_views

app_name = "jobtask"  # namespace
urlpatterns = [
    #url(r"taskdef/add$", jobtask_views.taskadd, name="taskdef-add"),
    url(r"taskdef/add$", jobtask_views.taskdef_add_view.as_view(), name="taskdef-add"),
    url(r'^taskdef/(?P<pk>\d+)$', jobtask_views.taskdef_detail_view.as_view(), name='taskdef-detail'),
    url(r'^taskdef/action$', jobtask_views.taskdef_action_view.as_view(), name='taskdef-action'),
    url(r"taskdef/list$", jobtask_views.taskdef_list_view.as_view(), name="taskdef-list"),
    # ajax
    url(r"taskdef/status$", jobtask_views.TaskStatus, name="taskdef-status"),
    url(r"taskdef/type$", jobtask_views.TaskType, name="taskdef-type"),
    url(r"taskdef/perm$", jobtask_views.TaskPerm, name="taskdef-perm"),
    url(r"taskdef/filetype$", jobtask_views.FileType, name="taskdef-filetype"),
]
