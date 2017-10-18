# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from book.models import  Author, Publisher, Book
from django.contrib.admin.templatetags.admin_list import date_hierarchy
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name","age", "email")
    search_fields = ("name",)
    
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name","addr")
    
class BookAdmin(admin.ModelAdmin):
    ## 表头显示的列
    list_display = ("title", "publisher", "publication_date")
    ## 列表页，右侧显示过滤block
    list_filter = ("publication_date", "title")
    ## 数据搜素
    search_fields = ("name",)
    ## 排序
    ordering = ("-publication_date", )
    ## 日期型字段按层次进行划分
    date_hierarchy = "publication_date"
    
    ###  查看、编辑单条数据的页面
    filter_horizontal = ("authors", )  # 仅仅对many-to-many字段有效
    #filter_vertical = ("authors",)
    ## 设置可编辑的字段，即此处设置publication_date为不可编辑
    #fields = ("title", "publisher", "authors")
    raw_id_fields = ("publisher", )  ## 仅仅对外键有效，当外键数量较多时，可通过这样来转换
    
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)