# -*- coding: utf-8 -*-
import types
from django import template    
register = template.Library()    
    
@register.filter(name='key')
def key(obj, k): 
    d = dict(obj)       
    return d.get(k, None)

@register.filter(name='get_attr_from_m')
def get_attr_from_m(model, attr): 
    return getattr(model, attr, None)

@register.filter(name='get_html_attr')
def get_html_attr(field, attrkey="attrs"): 
    attrs = getattr(field, attrkey, None)
    if type(attrs) != types.DictType: return ""
    tmplist = []
    for (k,v) in dict(attrs).iteritems():
        kvstr = '%s="%s"' % (k,v)
        tmplist.append(kvstr)
    attrstr = " ".join(tmplist)
    print attrstr
    return attrstr


@register.filter(name='gettype')
def gettype(field): 
    try:
        return field.get_internal_type()
    except:
        return None
    
@register.filter(name='is_auto_field')
def is_auto_field(field): 
    try:
        if field.get_internal_type() == "AutoField":return 1
        return 0
    except:
        return 1
    
@register.filter(name='is_text_field')
def is_text_field(field): 
    try:
        if field.get_internal_type() in ["CharField"]:return 1
        return 0
    except:
        return 1
    
@register.filter(name='is_textarea_field')
def is_textarea_field(field): 
    try:
        if field.get_internal_type() in ["TextField"]:return 1
        return 0
    except:
        return 1

@register.filter(name='is_datetime_field')
def is_datetime_field(field): 
    try:
        if field.get_internal_type() in ["DateTimeField", "DateField"]:return 1
        return 0
    except:
        return 1
    
@register.filter(name='is_int_field')
def is_int_field(field): 
    try:
        if field.get_internal_type() in ["SmallIntegerField", "IntegerField"]:return 1
        return 0
    except:
        return 1
    
@register.filter(name='is_input_field')
def is_input_field(field):
    if is_int_field(field) or is_text_field(field):return 1
    return 0

@register.filter(name="is_file_field")
def is_file_field(field):
    if field.get_internal_type() in ["FileField"]: return 1
    return 0
