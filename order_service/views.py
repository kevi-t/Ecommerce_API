from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import OrderSerializer
from .services import send_sms

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            customer = order.customer
            message = f"Dear {customer.name}, your order for {order.item} has been placed successfully."

            sms_response = send_sms(customer.phone_number, message)

            if sms_response:
                return Response({
                    'message': 'Order created successfully!',
                    'sms_response': sms_response
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'Order created successfully, but failed to send SMS.',
                    'sms_response': sms_response
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)