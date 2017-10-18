# coding: utf8
'''
Created on 2017年8月26日

@author: qiueer
'''

from django import forms

from django.db.models import FileField
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from .models import Task_Def

## take reference: 
## http://nemesisdesign.net/blog/coding/django-filefield-content-type-size-validation/
class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):        
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        tmpfile = data.file
        try:
            content_type = tmpfile.content_type
            if content_type in self.content_types:
                if tmpfile._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(tmpfile._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass        
            
        return data

class TaskDefForm(forms.ModelForm):
    class Meta(object):  ## 通用视图CreateView需要使用到
        model = Task_Def
        fields = "__all__"  # 效果与下列的相同
        #fields = ("file", "file_type", "main_script_name", "params", "executor", "task_status", "task_type", "task_perm_status", "func", "create_dt", "update_dt", "create_user")
        #exclude = ['create_dt', "update_dt", "create_user"]
        exclude = ['create_dt', "update_dt"]  ## 这两个字段在model中设置为auto_now_add和auto_now，是不可改变的，所以要排除掉
    
    ## for select fields
    task_status_map = [(-1, ""), (0, "停用"),(1, "启用")]
    task_type_map = [(-1, ""), (0, "系统任务"),(1, "普通任务")]
    task_perm_status_map = [(-1, ""), (0, "独享"),(1, "共享")]
    file_type_map = [(-1, ""), (0, "脚本"),(1, "脚本包")]
    
    #your_name = forms.CharField(label='Your name', max_length=100)
    #func = forms.Textarea() ## django_bootstrap2 目前不支持这种方式
    file = forms.FileField(label="文件路径", required=True)  #forms.CharField(max_length=255, label="文件路径")  #文件
    file_type = forms.IntegerField(label="文件类型", required=True, widget=forms.Select(choices=file_type_map))  # 脚本或脚本包
    main_script_name = forms.CharField(max_length=64, label="主脚本名", required=True, widget=forms.TextInput(attrs={'placeholder':u'例如check_route.sh...'}))
    #path = forms.CharField(max_length=255, label="文件路径")
    params = forms.CharField(max_length=64, label="参数", required=False, widget=forms.Textarea(attrs={'placeholder':u'such as: -p 1234 -k time', "rows": 3}))
    executor = forms.CharField(max_length=16, label="解析器", required=False)
    task_status = forms.IntegerField(label="任务状态", required=True, widget=forms.Select(choices=task_status_map))
    task_type = forms.IntegerField(label="任务类型", required=True, widget=forms.Select(choices=task_type_map))
    task_perm_status = forms.IntegerField(label="任务权限状态", required=True, widget=forms.Select(choices=task_perm_status_map))
    ## 下面的三个字段设置为HiddenInput，主要是为了可以post添加前可修改为当时的时间和当前的用户，不能不写
    create_dt = forms.DateTimeField(label="创建时间", widget=forms.HiddenInput())
    update_dt = forms.DateTimeField(label="更新时间", widget=forms.HiddenInput())
    create_user = forms.CharField(max_length=64, label="创建用户", widget=forms.HiddenInput())
    
    res_ctl_conf =  forms.IntegerField(label="主机资源控制", required=True, widget=forms.Select(choices=task_perm_status_map))
    func = forms.CharField(label="功能说明", required=True, widget=forms.Textarea(attrs={"rows": 3}))
    #func.widget.attrs["rows"] = 3
    note = forms.CharField( label="备注说明", required=False, widget=forms.Textarea(attrs={"rows": 3})) 
    # note.widget.attrs["rows"] = 3
   
    # 重写clean方法，增加文件大小校验
    def clean(self):
        data = super(TaskDefForm, self).clean()
        tmpfile = data.get("file", None)
        max_file_size = 20  # 20M
        if tmpfile.size / 1024 / 1024 > max_file_size:  #文件大小校验
            raise forms.ValidationError(u"文件大小不能大于%sM" % (max_file_size))
        return data
    

