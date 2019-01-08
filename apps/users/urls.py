#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-18'

from django.urls import path, re_path

from users.views import UserInfoView, UserAvatarUploadView, UserUpdatePwdView, SendEmailCodeView, UpdateEmailView, \
    MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

app_name = 'users'

urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    path('avatar/upload/', UserAvatarUploadView.as_view(), name='avatar_upload'),
    # 用户在个人中心修改密码
    path('update/pwd/', UserUpdatePwdView.as_view(), name='upload_pwd'),
    # 发送邮箱验证码
    path('send_email_code/', SendEmailCodeView.as_view(), name='send_email_code'),
    # 修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    path('my_course/', MyCourseView.as_view(), name='my_course'),
    # 我收藏的课程机构
    path('my_fav_org/', MyFavOrgView.as_view(), name='my_fav_org'),
    # 我收藏的讲师
    path('my_fav_teacher/', MyFavTeacherView.as_view(), name='my_fav_teacher'),
    # 我收藏的讲师
    path('my_fav_course/', MyFavCourseView.as_view(), name='my_fav_course'),
    # 我的消息
    path('my_message/', MyMessageView.as_view(), name='my_message'),
]
