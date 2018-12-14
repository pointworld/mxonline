from django.contrib import admin

from .models import UserProfile, EmailAuthCode, Slide


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'birthday', 'gender', 'address', 'mobile', 'avatar']
    search_fields = ['nickname', 'birthday', 'gender', 'address', 'mobile', 'avatar']
    list_filter = ['nickname', 'birthday', 'gender', 'address', 'mobile', 'avatar']


class EmailAuthCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class SlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailAuthCode, EmailAuthCodeAdmin)
admin.site.register(Slide, SlideAdmin)
