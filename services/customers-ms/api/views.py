from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import CustomerSerializer
from api.publisher import publish_customer_created

class CustomerCreateListView(APIView):
    def get(self, request):
        from api.models import Customer
        return Response(CustomerSerializer(Customer.objects.all(), many=True).data)

    def post(self, request):
        ser = CustomerSerializer(data=request.data)
        ser.is_valid(raise_tech=True)  # si usas raise_exception=True
        customer = ser.save()
        payload = CustomerSerializer(customer).data
        try:
            publish_customer_created(payload)
        except Exception as e:
            # loguea pero no rompas el 201 (o aplica "outbox pattern" si quieres 100% atómico)
            print("[publish_customer_created] error:", e)
        return Response(payload, status=status.HTTP_201_CREATED)
