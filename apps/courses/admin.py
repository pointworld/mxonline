from django.contrib import admin

from .models import Course, Lesson, Video, CourseResource


# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'detail', 'degree', 'duration', 'student_nums', 'fav_nums', 'cover',
                    'hit_nums', 'add_time']
    list_filter = ['name', 'desc', 'detail', 'degree', 'duration', 'student_nums', 'fav_nums', 'cover',
                   'hit_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'duration', 'student_nums', 'fav_nums', 'cover',
                     'hit_nums']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'add_time']
    list_filter = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']


class VideoAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'name', 'add_time']
    list_filter = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']


class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'download', 'add_time']
    list_filter = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
