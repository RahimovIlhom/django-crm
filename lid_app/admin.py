from django.contrib import admin

from lid_app.models import Lid, Contact


class LidAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'phone_number', 'course', 'group', 'balance', 'status']
    list_filter = ['course', 'group', 'status']
    search_fields = ['fullname', 'phone_number', 'location']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'phone_number', 'location', 'was_answered', 'created_time']
    list_filter = ['was_answered']
    search_fields = ['fullname', 'phone_number', 'location']


admin.site.register(Lid, LidAdmin)
admin.site.register(Contact, ContactAdmin)
