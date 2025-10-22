from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'package_type', 'status', 'created_at']
    list_filter = ['status', 'package_type', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'tracking_number']
    readonly_fields = ['created_at', 'updated_at']
