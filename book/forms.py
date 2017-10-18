# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

class AuthorForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(required=False)
    age = forms.CharField()