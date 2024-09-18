# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .serializers import OrderSerializer
# from .services import send_sms
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_order(request):
#     if request.method == 'POST':
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             message = f"Dear {customer.name}, your order for {order.item} has been placed successfully."
#             send_sms(customer.phone_number, message)
#         return Response({'message': 'Order created successfully!'}, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderSerializer
from .services import send_sms
from .models import Order

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Save the order
            order = serializer.save()

            # Fetch the customer object
            customer = order.customer
            message = f"Dear {customer.name}, your order for {order.item} has been placed successfully."

            # Send SMS
            send_sms(customer.phone_number, message)

            return Response({'message': 'Order created successfully!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)