#!/usr/bin/env python3
# _*_ coding: utf8 _*_

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q


from pure_pagination import Paginator, PageNotAnInteger

from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from .models import Course, CourseResource, Video


# Create your views here.


class CourseListView(View):
    """
    课程列表
    """

    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        # 热门
        hot_courses = Course.objects.all().order_by('-hit_nums')[:3]

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords)
                | Q(desc__icontains=search_keywords)
                | Q(detail__icontains=search_keywords)
            )

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-student_nums')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-fav_nums')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.hit_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag

        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
        else:
            related_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 点击数加一
        course.student_nums += 1
        course.save()

        # 查询用户是否已经关联了该课程
        course_users = UserCourse.objects.filter(user=request.user, course=course)
        if not course_users:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 取出学过该课程的所有用户
        course_users = UserCourse.objects.filter(course=course)
        # 取出学过该课程的所有用户的 id 列表
        user_ids = [course_user.user.id for course_user in course_users]
        # 取出该用户学过的所有课程
        user_all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出该用户学过的所有课程 id
        user_course_ids = [user_course.course.id for user_course in user_all_courses]
        # 获取该用户学过的其他所有课程
        related_courses = Course.objects.filter(id__in=user_course_ids).order_by('-hit_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'related_courses': related_courses,
        })


class CourseCommentsView(LoginRequiredMixin, View):
    """
    课程评论
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        course_users = UserCourse.objects.filter(user=request.user, course=course)
        if not course_users:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 取出学过该课程的所有用户
        course_users = UserCourse.objects.filter(course=course)
        # 取出学过该课程的所有用户的 id 列表
        user_ids = [course_user.user.id for course_user in course_users]
        # 取出该用户学过的所有课程
        user_all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出该用户学过的所有课程 id
        user_course_ids = [user_course.course.id for user_course in user_all_courses]
        # 获取该用户学过的其他所有课程
        related_courses = Course.objects.filter(id__in=user_course_ids).order_by('-hit_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)

        all_comments = CourseComments.objects.filter(course=course).order_by("-add_time")

        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'related_courses': related_courses,

            'all_comments': all_comments,
        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()

            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 查询用户是否已经关联了该课程
        course_users = UserCourse.objects.filter(user=request.user, course=course)
        if not course_users:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 取出学过该课程的所有用户
        course_users = UserCourse.objects.filter(course=course)
        # 取出学过该课程的所有用户的 id 列表
        user_ids = [course_user.user.id for course_user in course_users]
        # 取出该用户学过的所有课程
        user_all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出该用户学过的所有课程 id
        user_course_ids = [user_course.course.id for user_course in user_all_courses]
        # 获取该用户学过的其他所有课程
        related_courses = Course.objects.filter(id__in=user_course_ids).order_by('-hit_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'related_courses': related_courses,
            'video': video,
        })