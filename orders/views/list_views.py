from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.serializers import OrdersSerializer
from customer.models.models import Customer
from orders.models.models import Orders

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_orders(request):
    """
    Fetch all orders placed by the currently authenticated customer.
    """
    email = request.user.email  # Get the authenticated user's email

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch orders associated with this customer
    orders = Orders.objects.filter(customer=customer)

    # Serialize the orders
    serializer = OrdersSerializer(orders, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)