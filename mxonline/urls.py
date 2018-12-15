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

from users.views import index, LoginView, RegisterView, ActiveUserView

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),

    # 基于类方法实现登录页处理逻辑，as_view 是 View 类的一个类方法
    # 是 Main entry point for a request-response process
    # as_view 最终会返回一个 view
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # 图片验证码 url
    path('captcha/', include('captcha.urls')),
    # 邮箱激活
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
]
