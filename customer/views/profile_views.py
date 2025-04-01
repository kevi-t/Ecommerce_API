# customer/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from customer.models.models import Customer
from customer.serializers.profile_serializers import CustomerUpdateSerializer


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Allows an authenticated user to update their name and phone number.
    """
    email = request.user.email 

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerUpdateSerializer(customer, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully.',
            'customer': serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)