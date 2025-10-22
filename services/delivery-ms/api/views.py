from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Delivery
from .serializers import DeliverySerializer


class DeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar envíos
    Solo lectura - los envíos se crean automáticamente por eventos
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def list(self, request, *args, **kwargs):
        """
        Lista todos los envíos
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>[^/.]+)')
    def by_customer(self, request, customer_id=None):
        """
        Obtiene envíos por ID de cliente
        """
        deliveries = Delivery.objects.filter(customer_id=customer_id)
        serializer = self.get_serializer(deliveries, many=True)
        return Response({
            'count': deliveries.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Lista envíos pendientes
        """
        deliveries = Delivery.objects.filter(status='pending')
        serializer = self.get_serializer(deliveries, many=True)
        return Response({
            'count': deliveries.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def health(self, request):
        """
        Endpoint de health check
        """
        return Response({
            'status': 'healthy',
            'service': 'delivery-ms'
        })
