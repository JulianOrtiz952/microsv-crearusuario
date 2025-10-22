from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LoyaltyPoints
from .serializers import LoyaltyPointsSerializer


class LoyaltyPointsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar puntos de lealtad
    Solo lectura - los puntos se crean automáticamente por eventos
    """
    queryset = LoyaltyPoints.objects.all()
    serializer_class = LoyaltyPointsSerializer

    def list(self, request, *args, **kwargs):
        """
        Lista todos los registros de puntos
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
        Obtiene puntos por ID de cliente
        """
        try:
            loyalty = LoyaltyPoints.objects.get(customer_id=customer_id)
            serializer = self.get_serializer(loyalty)
            return Response(serializer.data)
        except LoyaltyPoints.DoesNotExist:
            return Response(
                {'error': 'No se encontraron puntos para este cliente'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def health(self, request):
        """
        Endpoint de health check
        """
        return Response({
            'status': 'healthy',
            'service': 'loyalty-ms'
        })
