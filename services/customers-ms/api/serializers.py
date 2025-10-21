from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_name(self, v):
        if len(v.strip()) < 2:
            raise serializers.ValidationError("El nombre es demasiado corto.")
        return v.strip()