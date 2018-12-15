# _*_ coding:utf8 _*_
from django.shortcuts import render
from django.views.generic.base import View

from organization.models import CourseOrg, CityDict


# Create your views here.


class OrgView(View):
    """
    课程机构列表的处理逻辑
    """

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        # 城市
        all_cities = CityDict.objects.all()
        return render(request, 'org-list.html', {
            'all_orgs': all_orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
        })