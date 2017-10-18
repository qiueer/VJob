# -*- coding: utf-8 -*-
from django import template    
register = template.Library()    
    
@register.filter(name='page_range')
def page_range(page_obj, size): 
    current_page = page_obj.number
    total_page = page_obj.paginator.num_pages
    a = (current_page - 1 ) / size
    begin = a * size + 1
    end = (a+1)* size 
    if end> total_page: end = total_page
    return range(begin, end+1)

