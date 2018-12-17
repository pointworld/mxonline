#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-17'

from django.urls import path, re_path

from courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentsView, AddCommentsView, VideoPlayView

app_name = 'courses'

urlpatterns = [
    # 课程列表
    path('list/', CourseListView.as_view(), name='course_list'),
    # 课程详情
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
    # 课程章节详情
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    re_path('comment/(?P<video_id>\d+)/', CourseCommentsView.as_view(), name='course_comment'),
    # 添加课程评论
    path('add_comment/', AddCommentsView.as_view(), name='add_comment'),
    # 添加课程评论
    re_path('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name='video_play'),
]
