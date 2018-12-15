# _*_ coding:utf8 _*_
from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict


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
