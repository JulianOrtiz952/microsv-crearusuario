from rest_framework import serializers
from .models import LoyaltyPoints


class LoyaltyPointsSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo LoyaltyPoints
    """
    class Meta:
        model = LoyaltyPoints
        fields = ['id', 'customer_id', 'customer_email', 'customer_name', 'points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
