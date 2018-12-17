# _*_ coding:utf8 _*_

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserConsultingForm
from courses.models import Course


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
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = 'course'
        # 根据 id 取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = 'desc'
        # 根据 id 取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        # 根据 id 取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
        })