#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-14 20:48'

from django import forms

from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    """
    登录模块的表单校验
    """

    # 这里的 username 和 password 必须和 html 表单中的一致
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """
    注册模块的表单校验
    """

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '无效的验证码'})


class ForgetForm(forms.Form):
    """
    忘记密码模块的表单校验
    """

    email = forms.EmailField(required=True)
    # 应用验证码 自定义错误输出 key 必须与异常一样
    captcha = CaptchaField(error_messages={'invalid': '无效的验证码'})


class ModifyPwdForm(forms.Form):
    """
    重置密码模块的表单校验
    """

    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)