from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from customer.models.models import Customer
from customer.serializers.register_serializers import CustomerSerializer
from customer.serializers.login_serializers import LoginSerializer
from customer.serializers.profile_serializers import CustomerUpdateSerializer


class CustomerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        if self.action == 'profile':
            return CustomerUpdateSerializer
        return CustomerSerializer

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Customer registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
            }, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'patch', 'put'], url_path='profile')
    def profile(self, request):
        try:
            customer = Customer.objects.get(email=request.user.email)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CustomerUpdateSerializer(customer)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)

        serializer = CustomerUpdateSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully.',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
