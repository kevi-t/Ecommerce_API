from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Orders
from orders.serializers import OrderSerializer
from orders.services import send_sms


class OrderViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet,):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        customer = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(customer=customer)
            message = (
                f"Dear {customer.name}, your order for {order.item} "
                "has been placed successfully."
            )
            sms_response = send_sms(customer.phone_number, message)

            if sms_response:
                msg = "Order created successfully!"
            else:
                msg = "Order created successfully, but failed to send SMS."

            return Response(
                {"message": msg, "sms_response": sms_response},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)