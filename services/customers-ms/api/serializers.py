from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Customer
    """
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        """
        Valida que el email sea único
        """
        if self.instance is None:  # Solo en creación
            if Customer.objects.filter(email=value).exists():
                raise serializers.ValidationError("Ya existe un cliente con este correo electrónico.")
        return value
