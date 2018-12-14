#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-14 20:48'

from django import forms


class LoginForm(forms.Form):

    # 这里的 username 和 password 必须和 html 表单中的一致
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
