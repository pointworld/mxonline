from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    # 用户信息
    path('info/', views.UserInfoView.as_view(), name="user_info"),

    # 用户头像上传
    path('image/upload/', views.UploadImageView.as_view(), name="image_upload"),

    # 用户个人中心修改密码
    path('update/pwd/', views.UpdatePwdView.as_view(), name="update_pwd"),

    # 专用于发送验证码
    path('sendemail_code/', views.SendEmailCodeView.as_view(), name="sendemail_code"),

    path('update_email/', views.UpdateEmailView.as_view(), name="update_email"),

    # 用户中心我的课程
    path('mycourse/', views.MyCourseView.as_view(), name="mycourse"),

    # 我收藏的课程机构
    path('myfav/org/',views.MyFavOrgView.as_view(), name="myfav_org"),

    # 我收藏的授课讲师
    path('myfav/teacher/', views.MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我收藏的课程
    path('myfav/course/', views.MyFavCourseView.as_view(), name="myfav_course"),

    # 我收藏的课程
    path('my_message/', views.MyMessageView.as_view(), name="my_message"),

]
