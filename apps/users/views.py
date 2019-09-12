import json

from django.urls import reverse
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
# 进行密码加密
from django.contrib.auth.hashers import make_password
# 基于类实现需要继承的 view
from django.views.generic.base import View

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users.models import UserProfile, EmailVerifyRecord, Banner
from users.forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm

# 异步发送邮件
from users.tasks import send_register_email


class ActiveUserView(View):
    """激活用户的 view"""

    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的 user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        # 自己瞎输的验证码
        else:
            return render(
                request, "register.html", {
                    "msg": "您的激活链接无效", "active_form": active_form})


class RegisterView(View):
    """注册功能的 view"""

    def get(self, request):
        """返回用户注册页面"""

        # 添加验证码
        register_form = RegisterForm()

        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        """处理用户注册表单"""

        # 实例化 form
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            # 这里注册时前端的 name 为 email
            user_name = request.POST.get("email", "")

            # 用户查重
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已存在"})

            pass_word = request.POST.get("password", "")

            # 实例化一个 user_profile 对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            # 默认激活状态为 false
            user_profile.is_active = False

            # 加密 password 进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册点生慕课小站!! --系统自动消息"
            user_message.save()

            # 发送注册激活邮件
            send_register_email.delay(user_name, "register")

            # 跳转到登录页面
            return render(request, "login.html")
        # 注册邮箱 form 验证失败
        else:
            return render(
                request, "register.html", {
                    "register_form": register_form})


class LogoutView(View):
    def get(self, request):
        # django 自带的 logout
        logout(request)
        # 重定向到首页
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        # render 就是渲染 html 返回用户
        # render 三变量: request 模板名称 一个字典写明传给前端的值
        redirect_url = request.GET.get('next', '')
        return render(request, "login.html", {"redirect_url": redirect_url})

    def post(self, request):
        # 类实例化需要一个字典参数 dict: request.POST 就是一个 QueryDict 所以直接传入
        # POST 中的 username password，会对应到 form 中
        login_form = LoginForm(request.POST)

        # is_valid 判断我们字段是否有错执行我们原有逻辑，验证失败跳回 login 页面
        if login_form.is_valid():
            # 取不到时为空，username，password 为前端页面 name 值
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回 user 对象，失败返回 null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是 null 说明验证成功
            if user is not None:
                # 只有当用户激活时才给登录
                if user.is_active:
                    # login 两参数：request, user
                    # 实际是对 request 写了一部分东西进去，然后在 render 的时候：
                    # request 是要 render 回去的。这些信息也就随着返回浏览器。完成登录
                    login(request, user)
                    # 跳转到首页 user request 会被带回到首页
                    # 增加重定向回原网页
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    # 跳转到首页 user request 会被带回到首页
                    return HttpResponseRedirect(reverse("index"))
                # 即用户未激活跳转登录，提示未激活
                else:
                    return render(request, "login.html", {"msg": "用户名未激活! 请前往邮箱进行激活"})
            # 仅当用户真的密码出错时
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        # 验证不成功跳回登录页面
        # 没有成功说明里面的值是 None，并再次跳转回主页面
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPwdView(View):
    """用户忘记密码的处理"""

    def get(self, request):
        # 给忘记密码页面加上验证码
        active_form = ActiveForm(request.POST)
        return render(request, "forgetpwd.html", {"active_form": active_form})

    # post方法实现
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # form验证合法情况下取出email
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送找回密码邮件
            send_register_email.delay(email, "forget")
            # 发送完毕返回登录页面并显示发送邮件成功。
            return render(request, "login.html", {"msg": "重置密码邮件已发送,请注意查收"})
        # 如果表单验证失败也就是他验证码输错等。
        else:
            return render(
                request, "forgetpwd.html", {
                    "forget_form": forget_form})


class ResetView(View):
    """
    重置密码的 view
    忘记密码后不需要找回密码（不安全），直接引导用户重置密码，或发送一个简单的临时密码给用户也是可以的
    """

    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 将 email 传回来
                # 只传回 active_code
                return render(request, "password_reset.html", {"active_code": active_code})
        # 自己瞎输的验证码
        else:
            return render(
                request, "forgetpwd.html", {
                    "msg": "您的重置密码链接无效,请重新请求", "active_form": active_form})


class ModifyPwdView(View):
    """修改密码"""

    def post(self, request):
        modiypwd_form = ModifyPwdForm(request.POST)

        if modiypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            active_code = request.POST.get("active_code", "")
            email = request.POST.get("email", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            # 如果密码一致
            # 找到激活码对应的邮箱
            all_record = EmailVerifyRecord.objects.filter(code=active_code)
            for record in all_record:
                email = record.email
            user = UserProfile.objects.get(email=email)
            # 加密成密文
            user.password = make_password(pwd2)
            # save 保存到数据库
            user.save()
            return render(request, "login.html", {"msg": "密码修改成功，请登录"})
        # 验证失败说明密码位数不够
        else:
            email = request.POST.get("email", "")
            return render(
                request, "password_reset.html",
                {"email": email, "modiypwd_form": modiypwd_form}
            )


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "usercenter-info.html", {})

    def post(self, request):
        """更新用户信息"""

        user_info_form = UserInfoForm(request.POST, instance=request.user)

        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 通过 json 的 dumps 方法把字典转换为 json 字符串
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """用户上传图片的 view: 用于修改头像"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        # 这时候用户上传的文件就已经被保存到 imageform 了 ，为 modelform 添加 instance 值直接保存
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """在个人中心修改用户密码"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            # 如果密码一致
            user = request.user
            # 加密成密文
            user.password = make_password(pwd2)
            # save 保存到数据库
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        # 验证失败说明密码位数不够
        else:
            # 通过 json 的 dumps 方法把字典转换为 json 字符串
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """发送邮箱验证码的 view"""

    def get(self, request):
        # 取出需要发送的邮件
        email = request.GET.get("email", "")

        # 不能是已注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email.delay(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """修改邮箱的 view"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """个人中心页我的课程"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """我收藏的机构"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的 fav_orgs 只是存放了 id。我们还需要通过 id 找到机构对象
        for fav_org in fav_orgs:
            # 取出 fav_id 也就是机构的id
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """我收藏的授课讲师"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """我收藏的课程"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """我的消息"""

    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人中心消息页面，清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对消息进行分页
        # 尝试获取前台 get 请求传递过来的 page 参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 这里指从 all_message 中取五个出来，每页显示 5 个
        p = Paginator(all_message, 4)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
        })


class IndexView(View):
    """首页 view"""

    def get(self, request):
        # 取出轮播图
        all_banner = Banner.objects.all().order_by('index')[:5]
        # 正常位课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播图课程取三个
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "all_banner": all_banner,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })
