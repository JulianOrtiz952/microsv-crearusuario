from django.contrib import admin
from .models import LoyaltyPoints


@admin.register(LoyaltyPoints)
class LoyaltyPointsAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'customer_name', 'customer_email', 'points', 'created_at']
    list_filter = ['created_at', 'points']
    search_fields = ['customer_name', 'customer_email']
    readonly_fields = ['created_at', 'updated_at']
