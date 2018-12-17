#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-17'

from django.urls import path, include, re_path

from organization.views import OrgView, AddUserConsultingView


app_name = 'organization'

urlpatterns = [
    # 课程机构首页
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_consulting/', AddUserConsultingView.as_view(), name='add_consulting'),
]