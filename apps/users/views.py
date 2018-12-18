# _*_ coding: utf8 _*_
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
# Encapsulate filters as objects that can then be combined logically (using
#     `&` and `|`).
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from utils.mixin_utils import LoginRequiredMixin
from .models import UserProfile, EmailAuthCode
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UserAvatarUploadForm, UserInfoForm
from utils.email_send import send_register_or_forget_email

"""
Create your views here.
Django 的 view 实际就是一个函数，接收 request 请求对象，处理后返回 response 对象
当 url 被相应的 view 函数处理时，view 的第一个参数需要传入 request 对象
"""


def index(request):
    """
    首页的处理逻辑
    :param request:
    :return: response
    """
    return render(request, 'index.html', {})


class RegisterView(View):
    """
    注册模块的处理逻辑
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

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = 'Welcome register GMOOC.'

            # 发送注册激活邮件
            send_register_or_forget_email(username, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    """
    登录模块的处理逻辑
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


class ActiveUserView(View):
    """
    激活用户模块的处理逻辑
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


class ForgetPwdView(View):
    """
    忘记密码模块的处理逻辑
    """

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码邮件
            send_register_or_forget_email(email, 'forget')
            # 发送完毕返回登录页面并显示发送邮件成功
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ModifyPwdView(View):
    """
    重置密码模块的处理逻辑
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致！'})
            user = UserProfile.objects.get(email=email)
            # 加密成密文
            user.password = make_password(pwd2)
            # 保存到数据库
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class ResetPwdView(View):
    """
    重置密码模块的处理逻辑
    """

    def get(self, request, active_code):
        # 查询邮箱验证码是否存在
        all_records = EmailAuthCode.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


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


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UserAvatarUploadView(LoginRequiredMixin, View):
    """
    用户修改头像
    """

    def post(self, request):
        avatar_form = UserAvatarUploadForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if avatar_form.is_valid():
            avatar_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UserUpdatePwdView(View):
    """
    用户在个人中心修改密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg": "密码不一致"}', content_type='application/json')
            user = request.user
            # 加密成密文
            user.password = make_password(pwd2)
            # 保存到数据库
            user.save()

            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已经存在"}', content_type='application/json')

        send_register_or_forget_email(email, 'update_email')
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailAuthCode.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    用户收藏的课程机构
    """

    def get(self, request):
        org_list = []
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in user_fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'user_fav_orgs': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    用户收藏的讲师
    """

    def get(self, request):
        teahcer_list = []
        user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in user_fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teahcer_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'user_fav_teachers': teahcer_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    用户收藏的课程
    """

    def get(self, request):
        course_list = []
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in user_fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'user_fav_courses': course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    用户的消息
    """

    def get(self, request):
        all_messages = UserMessage.objects.filter(receiver=request.user.id)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_messages, 2, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })
