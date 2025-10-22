from rest_framework import serializers
from .models import EmailLog


class EmailLogSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo EmailLog
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    email_type_display = serializers.CharField(source='get_email_type_display', read_only=True)
    
    class Meta:
        model = EmailLog
        fields = [
            'id', 'customer_id', 'customer_email', 'customer_name',
            'email_type', 'email_type_display', 'subject', 'body',
            'status', 'status_display', 'error_message',
            'created_at', 'sent_at'
        ]
        read_only_fields = ['id', 'created_at', 'sent_at']
