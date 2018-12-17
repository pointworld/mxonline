#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-17'

from django.urls import path, include, re_path

from courses.views import CourseListView


app_name = 'courses'

urlpatterns = [
    path('list/', CourseListView.as_view(), name='course_list'),
]
