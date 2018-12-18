#!/usr/bin/env python3
# _*_ coding: utf8 _*_

__author__ = 'point'
__date__ = '2018-12-18'

from django.urls import path, re_path

from users.views import UserInfoView, UserAvatarUploadView, UserUpdatePwdView, SendEmailCodeView, UpdateEmailView

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
]
