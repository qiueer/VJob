# -*- coding: utf-8 -*-
from __future__ import unicode_literals


#from .control.TaskDef import add as taskadd
from .control.TaskDef import AddView as taskdef_add_view
from .control.TaskDef import ListView as taskdef_list_view
from .control.TaskDef import DetailView as taskdef_detail_view
from .control.TaskDef import ActionView as taskdef_action_view
from .control.Ajax import TaskStatus
from .control.Ajax import TaskType
from .control.Ajax import TaskPerm
from .control.Ajax import FileType