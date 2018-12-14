# _*_ coding: utf8 _*_

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
# Encapsulate filters as objects that can then be combined logically (using
#     `&` and `|`).
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile

"""
Create your views here.
Django 的 view 实际就是一个函数，接收 request 请求对象，处理后返回 response 对象
当 url 被相应的 view 函数处理时，view 的第一个参数需要传入 request 对象
"""


class LoginView(View):
    """
    登录页处理类
    调用时会自动判断 request.method == 'GET' 或 request.method == 'POST'
    然后调用下面定义的 get 方法或 post 方法来处理登录逻辑
    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        return render(request, 'login.html', {})

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 验证成功返回 user 对象否则返回 None
        user = authenticate(username=username, password=password)
        # 用户存在则跳转到首页
        if user is not None:
            # login 函数接收两个参数：request、user，函数会对 request 做处理，
            # 使 request 携带有 user 等信息
            login(request, user)
            # 这些信息会被处理成响应，最终返回到浏览器，完成登录
            return render(request, 'index.html', {})
        # 用户不存在则重新跳转到登录页
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误！'})


class CustomBackend(ModelBackend):
    """
    自定义 authenticate 方法，使其支持使用用户名或邮箱登录
    继承 ModelBackend 类，因为它有方法 authenticate，可点进源码查看
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django 的后台中密码是被加密的：所以不能用 password==password 做判断
            # UserProfile 继承的 AbstractUser 中有 def check_password(self, raw_password)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def index(request):
    """
    首页处理函数
    :param request:
    :return: response
    """
    return render(request, 'index.html', {})

