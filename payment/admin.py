from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'payment_type', 'created_time', 'update_time']
    list_filter = ['student', 'payment_type', 'amount']
    search_fields = ['student']


admin.site.register(Payment, PaymentAdmin)
