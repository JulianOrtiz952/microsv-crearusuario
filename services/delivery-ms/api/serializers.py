from rest_framework import serializers
from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Delivery
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'customer_id', 'customer_email', 'customer_name', 'customer_address',
            'package_type', 'status', 'status_display', 'tracking_number',
            'created_at', 'updated_at', 'shipped_at', 'delivered_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
