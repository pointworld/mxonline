# _*_ coding: utf8 _*_

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
# Encapsulate filters as objects that can then be combined logically (using
#     `&` and `|`).
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile, EmailAuthCode
from .forms import LoginForm, RegisterForm
from utils.email_send import send_register_email

"""
Create your views here.
Django 的 view 实际就是一个函数，接收 request 请求对象，处理后返回 response 对象
当 url 被相应的 view 函数处理时，view 的第一个参数需要传入 request 对象
"""


def index(request):
    """
    首页处理函数
    :param request:
    :return: response
    """
    return render(request, 'index.html', {})


class ActiveUserView(View):
    """

    """

    def get(self, request, active_code):
        all_records = EmailAuthCode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    """
    注册
    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        # 生成输入框+验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        """

        :param request:
        :return:
        """
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {
                    'msg': '用户已经存在！',
                    'register_form': register_form,
                })
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.password = make_password(password)
            user_profile.is_active = False
            # 发送注册邮件之前先保存到数据库，到时候查询链接是否存在
            user_profile.save()

            # 发送注册激活邮件
            send_register_email(username, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


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
        # 类实例化需要一个字典参数，而 request.POST 就是一个 QueryDict 所以直接传入
        # POST 中的 username password，会对应到 form 中
        # 实例化 LoginView 时，会对表单字段进行了验证
        login_form = LoginForm(request.POST)

        # is_valid 判断我们表单字段是否有效，有效则执行我们原有逻辑
        if login_form.is_valid():

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 验证成功返回 user 对象否则返回 None
            user = authenticate(username=username, password=password)
            # 用户存在则跳转到首页
            if user is not None:
                if user.is_active:
                    # login 函数接收两个参数：request、user，函数会对 request 做处理，
                    # 使 request 携带有 user 等信息
                    login(request, user)
                    # 这些信息会被处理成响应，最终返回到浏览器，完成登录
                    return render(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！'})
            # 用户不存在则重新跳转到登录页
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        # 表单字段无效则跳回 login 页面，减轻对数据库查询的负担
        else:
            return render(request, 'login.html', {'login_form': login_form})


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


