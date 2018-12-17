#!/usr/bin/env python3
# _*_ coding: utf8 _*_

from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course

# Create your views here.


class CourseListView(View):
    """
    课程列表
    """

    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        # 热门
        hot_courses = Course.objects.all().order_by('-hit_nums')[:3]

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-student_nums')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-hit_nums')

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