#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-17'

import re

from django import forms

from operation.models import UserConsulting


class UserConsultingForm(forms.ModelForm):

    class Meta:
        model = UserConsulting
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        REGEXP_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEXP_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')