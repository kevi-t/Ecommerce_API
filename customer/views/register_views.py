# customer/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from ..serializers.register_serializers import CustomerSerializer


# Registration logic
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Customer registered successfully!'}, status=status.HTTP_201_CREATED)
        
        formatted_errors = {
            field: messages for field, messages in serializer.errors.items()
        }
        return Response({"errors": formatted_errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)