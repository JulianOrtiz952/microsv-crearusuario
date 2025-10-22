from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import EmailLog
from .serializers import EmailLogSerializer


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar logs de emails
    Solo lectura - los emails se envían automáticamente por eventos
    """
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer

    def list(self, request, *args, **kwargs):
        """
        Lista todos los logs de emails
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
        Obtiene logs de emails por ID de cliente
        """
        emails = EmailLog.objects.filter(customer_id=customer_id)
        serializer = self.get_serializer(emails, many=True)
        return Response({
            'count': emails.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def sent(self, request):
        """
        Lista emails enviados exitosamente
        """
        emails = EmailLog.objects.filter(status='sent')
        serializer = self.get_serializer(emails, many=True)
        return Response({
            'count': emails.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def failed(self, request):
        """
        Lista emails que fallaron
        """
        emails = EmailLog.objects.filter(status='failed')
        serializer = self.get_serializer(emails, many=True)
        return Response({
            'count': emails.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def health(self, request):
        """
        Endpoint de health check
        """
        return Response({
            'status': 'healthy',
            'service': 'email-ms'
        })
