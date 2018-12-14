from django.contrib import admin

from .models import UserConsulting, CourseComments, UserFavorite, UserMessage, UserCourse


# Register your models here.


class UserConsultingAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['receiver', 'message', 'has_read', 'add_time']
    list_filter = ['receiver', 'message', 'has_read', 'add_time']
    search_fields = ['receiver', 'message', 'has_read']


class CourseCommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'fav_type', 'add_time']
    list_filter = ['user_id', 'fav_type', 'add_time']
    search_fields = ['user_id', 'fav_type']


admin.site.register(UserConsulting, UserConsultingAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(CourseComments, CourseCommentsAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
