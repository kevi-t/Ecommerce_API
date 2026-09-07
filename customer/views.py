import requests
from django.conf import settings
from django.contrib.auth import login as django_login
from django.shortcuts import redirect
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from customer.models import Customer
from customer.serializers import (CustomerLoginSerializer,CustomerProfileUpdateSerializer,
                                  CustomerRegistrationSerializer,CustomerSerializer,)


@api_view(["GET"])
@permission_classes([AllowAny])
def success(request):
    return Response({"message": "Success"}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def oidc_login(request):
    authorization_url = (
        f"{settings.OIDC_OP_AUTHORIZATION_ENDPOINT}"
        f"?response_type=code"
        f"&client_id={settings.OIDC_RP_CLIENT_ID}"
        f"&redirect_uri={settings.LOGIN_REDIRECT_URL}"
        f"&scope=openid email profile"
    )
    return redirect(authorization_url)

@api_view(["GET"])
@permission_classes([AllowAny])
def oidc_callback(request):
    code = request.GET.get("code")
    if not code:
        return Response(
            {"error": "No authorization code received"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.LOGIN_REDIRECT_URL,
        "client_id": settings.OIDC_RP_CLIENT_ID,
        "client_secret": settings.OIDC_RP_CLIENT_SECRET,
    }
    token_response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data=token_data)
    if token_response.status_code != 200:
        return Response(
            {"error": "Failed to fetch token"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    access_token = token_response.json().get("access_token")
    userinfo_response = requests.get(
        settings.OIDC_OP_USERINFO_ENDPOINT,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if userinfo_response.status_code != 200:
        return Response(
            {"error": "Failed to fetch user info"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    userinfo = userinfo_response.json()
    email = userinfo.get("email")
    if not email:
        return Response(
            {"error": "Invalid OpenID response"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user, created = Customer.objects.get_or_create(
        email=email,
        defaults={
            "name": userinfo.get("name", "Unknown"),
            "phone_number": userinfo.get("phone_number", ""),
        },
    )
    if created:
        user.set_unusable_password()
        user.save()

    user.backend = "django.contrib.auth.backends.ModelBackend"
    django_login(request, user)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "message": "Authentication successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_200_OK,
    )


class CustomerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CustomerRegistrationSerializer
        if self.action == "register":
            return CustomerRegistrationSerializer
        if self.action == "login":
            return CustomerLoginSerializer
        if self.action == "profile" and self.request.method in {"PATCH", "PUT"}:
            return CustomerProfileUpdateSerializer
        return CustomerSerializer

    def get_permissions(self):
        if self.action in ["create", "register", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Customer registered successfully!"},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def register(self, request):
        return self.create(request)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "status": "success",
                "data": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get", "patch", "put"], url_path="profile")
    def profile(self, request):
        customer = request.user

        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        return Response(
            {
                "status": "success",
                "message": "Profile updated successfully.",
                "data": CustomerSerializer(customer).data,
            },
            status=status.HTTP_200_OK,
        )