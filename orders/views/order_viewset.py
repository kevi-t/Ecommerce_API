from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models.models import Customer
from orders.models.models import Orders
from orders.serializers.serializers import OrdersSerializer
from orders.services import send_sms


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            customer = Customer.objects.get(email=self.request.user.email)
            return Orders.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Orders.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(email=request.user.email)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['customer'] = customer.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            message = f"Dear {customer.name}, your order for {order.item} has been placed successfully."
            sms_response = send_sms(customer.phone_number, message)

            msg = 'Order created successfully!' if sms_response else 'Order created successfully, but failed to send SMS.'
            return Response({'message': msg, 'sms_response': sms_response}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
