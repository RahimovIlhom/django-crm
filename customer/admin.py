from django.contrib import admin

from .models import Mentor, Student


class MentorAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'phone_number', 'course']
    list_filter = ['course']
    search_fields = ['fullname', 'phone_number', 'location']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'phone_number', 'course', 'group', 'balance', 'status']
    list_filter = ['course', 'group', 'status']
    search_fields = ['fullname', 'phone_number', 'location']


admin.site.register(Mentor, MentorAdmin)
admin.site.register(Student, StudentAdmin)
