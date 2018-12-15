# _*_ coding:utf8 _*_
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


class OrgView(View):
    """
    课程机构列表的处理逻辑
    """

    def get(self, request):
        return render(request, 'org-list.html', {})