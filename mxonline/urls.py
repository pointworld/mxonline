"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# Serve static files below a given point in the directory structure
from django.views.static import serve

from mxonline.settings import MEDIA_ROOT
from users.views import index, LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 首页
    path('', index, name='index'),
    # 登录
    path('login/', LoginView.as_view(), name='login'),
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    # 图片验证码
    path('captcha/', include('captcha.urls')),
    # 邮箱激活
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(),
            name='user_active'),
    # 忘记密码
    path('forget/', ForgetPwdView.as_view(), name='forget_psd'),
    # 密码重置
    re_path('reset/(?P<active_code>.*)/', ResetPwdView.as_view(),
            name='reset_pwd'),
    # 修改密码
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_psd'),

    # 课程机构 url 配置
    path('org/', include('organization.urls', namespace='org')),

    # 课程相关 url 配置
    path('course/', include('courses.urls', namespace='course')),

    # 用户相关 url 配置
    path('users/', include('users.urls', namespace='users')),

    # 上传文件的访问处理
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
]
