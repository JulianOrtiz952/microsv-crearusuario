from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Customer
from .serializers import CustomerSerializer
from .producer import producer
import logging

logger = logging.getLogger(__name__)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes
    Proporciona operaciones CRUD y publica eventos a RabbitMQ
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo cliente y publica evento a RabbitMQ
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guardar cliente en base de datos
        customer = serializer.save()
        
        # Publicar evento a RabbitMQ de forma asíncrona
        try:
            customer_data = customer.to_dict()
            producer.publish_customer_created(customer_data)
            logger.info(f"Cliente creado y evento publicado: {customer.email}")
        except Exception as e:
            logger.error(f"Error publicando evento: {str(e)}")
            # No fallar la creación si falla la publicación
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def list(self, request, *args, **kwargs):
        """
        Lista todos los clientes
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """
        Obtiene un cliente por ID
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def health(self, request):
        """
        Endpoint de health check
        """
        return Response({
            'status': 'healthy',
            'service': 'customers-ms'
        })
