from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

import xadmin

from users import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # 自定义 admin 的后台
    path('xadmin/', xadmin.site.urls),

    # 首页
    path('', views.IndexView.as_view(), name="index"),

    # 登录
    path('login/', views.LoginView.as_view(), name="login"),

    # 退出
    path('logout/', views.LogoutView.as_view(), name="logout"),

    # 注册
    path("register/", views.RegisterView.as_view(), name="register"),

    # 验证码
    path("captcha/", include('captcha.urls')),

    # 激活用户
    re_path('active/(?P<active_code>.*)/', views.ActiveUserView.as_view(), name="user_active"),

    # 忘记密码
    path('forget/', views.ForgetPwdView.as_view(), name="forget_pwd"),

    # 重置密码：用来接收来自邮箱的重置链接
    re_path('reset/(?P<active_code>.*)/', views.ResetView.as_view(), name="reset_pwd"),

    # 修改密码：用于password reset 页面提交表单
    path('modify_pwd/', views.ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构和讲师 app 的 url 配置
    path("org/", include('organization.urls', namespace='org')),

    # 课程 app 的 url 配置
    path("course/", include('courses.urls')),

    # user app 的 url 配置
    path("users/", include('users.urls', namespace="users")),

    # 富文本相关
    path('ueditor/', include('DjangoUeditor.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
