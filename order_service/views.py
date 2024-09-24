from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderSerializer
from .services import send_sms
from customer_service.models import Customer  # Adjust based on your actual import

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    email = request.user.email  # Get the authenticated user's email

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data['customer'] = customer.id  # Set the customer ID from the retrieved Customer instance

    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        order = serializer.save()
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