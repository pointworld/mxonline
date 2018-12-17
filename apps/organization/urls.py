#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-17'

from django.urls import path, re_path

from .views import OrgView, AddUserConsultingView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView


app_name = 'organization'

urlpatterns = [
    # 课程机构首页
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_consulting/', AddUserConsultingView.as_view(), name='add_consulting'),
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name='org_home'),
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='org_course'),
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='org_desc'),
    re_path('org/teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='org_teacher'),
    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name='add_fav'),

    # 讲师相关 url 配置

    # 讲师列表
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    # 讲师详情
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name='teacher_detail'),
]