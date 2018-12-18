#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-18'

from django.urls import path, re_path

from users.views import UserInfoView, UserAvatarUploadView, UserUpdatePwdView

app_name = 'users'

urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    path('avatar/upload/', UserAvatarUploadView.as_view(), name='avatar_upload'),
    # 用户 在个人中心修改密码
    path('update/pwd/', UserUpdatePwdView.as_view(), name='upload_pwd'),

]
