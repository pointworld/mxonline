# _*_ coding:utf8 _*_

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from .forms import UserConsultingForm
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.


class OrgView(View):
    """
    课程机构列表的处理逻辑
    """

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        # 热门机构
        hot_orgs = all_orgs.order_by('-hit_nums')[:3]

        # 城市
        all_cities = CityDict.objects.all()

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords)
                | Q(desc__icontains=search_keywords)
            )

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'learners':
                all_orgs = all_orgs.order_by('-learners')
            elif sort == 'course_nums':
                all_orgs = all_orgs.order_by('-course_nums')

        # 当前机构数量
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class AddUserConsultingView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        user_consulting_form = UserConsultingForm(request.POST)
        if user_consulting_form.is_valid():
            # modelform 和 form 的区别
            # modelform 有 model 的属性
            # 当 commit 为 true 进行真正保存
            # 这样就不需要把每个字段都取出来然后存到 model 的对象中之后 save
            user_consulting = user_consulting_form.save(commit=True)
            # 表单验证通过，返回 json 字符串，异步不刷新
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            # 表单验证不通过，返回 json 字符串，并将 form 的报错信息通过 msg 传递到前端
            return HttpResponse(
                '{"status": "fail", "msg": "添加出错"}',
                content_type='application/json'
            )


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = 'home'
        # 根据 id 取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 点击数加一
        course_org.hit_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = 'course'
        # 根据 id 取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=1):
                has_fav = True

        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = 'desc'
        # 根据 id 取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        # 根据 id 取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """
    用户收藏和取消收藏
    """

    def post(self, request):
        # 收藏的课程，讲师，机构的 id
        # 默认值取 0 是因为空串转 int 会报错
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户的登录状态：即使没有登录也会有一个匿名的 user
        if not request.user.is_authenticated:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()

            # 收藏数减一
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                # 收藏数加一
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    讲师列表
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords)
                | Q(post__icontains=search_keywords)
                | Q(company__icontains=search_keywords)
            )

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-hit_nums')

        sorted_teacher = Teacher.objects.all().order_by('-hit_nums')[:3]

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 2, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sorted_teacher': sorted_teacher,
            'sort': sort,
        })


class TeacherDetailView(View):
    """
    讲师详情
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)

        # 点击数加一
        teacher.hit_nums += 1
        teacher.save()

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user.id, fav_type=3, fav_id=int(teacher_id)):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user.id, fav_type=2, fav_id=int(teacher.org.id)):
            has_org_faved = True

        # 讲师排行
        sorted_teacher = Teacher.objects.all().order_by('-hit_nums')[:3]

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,
        })