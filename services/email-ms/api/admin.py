from django.contrib import admin
from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'email_type', 'status', 'created_at', 'sent_at']
    list_filter = ['status', 'email_type', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'subject']
    readonly_fields = ['created_at', 'sent_at']
