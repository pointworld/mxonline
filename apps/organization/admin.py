from django.contrib import admin

from .models import CityDict, CourseOrg, Teacher


# Register your models here.


class CityDictAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']


class CourseOrgAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'hit_nums', 'fav_nums', 'cover', 'address', 'city', 'add_time']
    list_filter = ['name', 'desc', 'hit_nums', 'fav_nums', 'cover', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'hit_nums', 'fav_nums', 'cover', 'address', 'city']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'org', 'work_years', 'company', 'post', 'style',
                    'hit_nums', 'fav_nums', 'add_time']
    list_filter = ['name', 'gender', 'org', 'work_years', 'company', 'post', 'style',
                   'hit_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'gender', 'org', 'work_years', 'company', 'post', 'style',
                     'hit_nums', 'fav_nums']


admin.site.register(CityDict, CityDictAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)
