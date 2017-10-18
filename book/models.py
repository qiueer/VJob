# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField(verbose_name=u"邮箱",  blank=True) #可以留空
    age = models.IntegerField()
    
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    country = models.CharField(max_length=64)
    state_province = models.CharField(max_length=32)
    website = models.CharField(max_length=32,null=True)
    
    ## python 3
    def __str__(self):
        return unicode(self.name)
    
    ## python 2
    def __unicode__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=64, verbose_name=u"书名")
    authors = models.ManyToManyField(Author, verbose_name=u"作者")
    publisher = models.ForeignKey(Publisher, verbose_name=u"出版社")
    publication_date = models.DateTimeField(blank=True, null=True, verbose_name="出版时间")
    


    