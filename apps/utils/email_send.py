#!/usr/bin/env python3
# _*_ coding: utf8 _*_

from random import Random

# 导入 Django 自带的邮件模块下的 send_mail 方法
from django.core.mail import send_mail

# 导入 setting 中发送邮件的配置
from mxonline.settings import EMAIL_FROM

__author__ = 'point'
__date__ = '2018-12-15'


from users.models import EmailAuthCode


def random_str(random_length=8):
    """
    # 生成指定长度的随机字符串
    :param random_length:
    :return:
    """
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

def send_register_or_forget_email(email, send_type='register'):
    """
    发送注册邮件
    :param email:
    :param send_type:
    :return:
    """
    email_record = EmailAuthCode()
    # 生成随机的 code 放入链接
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        # 使用 Django 内置函数完成邮件发送。
        # 四个参数：主题，邮件内容，发送者，接收者 list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功为 True 否则 False
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '慕学在线网重置密码链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功为 True 否则 False
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = '慕学在线网邮箱修改验证码'
        email_body = '你的邮箱验证码为：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功为 True 否则 False
        if send_status:
            pass



