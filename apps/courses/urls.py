#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-17'

from django.urls import path, re_path

from courses.views import CourseListView, CourseDetailView

app_name = 'courses'

urlpatterns = [
    # 课程列表
    path('list/', CourseListView.as_view(), name='course_list'),
    # 课程详情
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
]
