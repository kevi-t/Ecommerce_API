# customer/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login as django_login


import requests
from ..models.models import Customer

# ✅ OpenID Connect (Google Login Redirect)
@api_view(['GET'])
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


# ✅ OpenID Callback (Handles Google Response)
@api_view(['GET'])
@permission_classes([AllowAny])
def oidc_callback(request):
    code = request.GET.get('code')
    if not code:
        return Response({'error': 'No authorization code received'}, status=status.HTTP_400_BAD_REQUEST)

    # Exchange code for tokens
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.LOGIN_REDIRECT_URL,
        'client_id': settings.OIDC_RP_CLIENT_ID,
        'client_secret': settings.OIDC_RP_CLIENT_SECRET,
    }
    token_response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data=token_data)
    print(token_response.json())
    if token_response.status_code != 200:
        return Response({'error': 'Failed to fetch token'}, status=status.HTTP_400_BAD_REQUEST)

    access_token = token_response.json().get('access_token')

    # Fetch user info from OpenID provider
    userinfo_response = requests.get(settings.OIDC_OP_USERINFO_ENDPOINT, headers={'Authorization': f'Bearer {access_token}'})
    if userinfo_response.status_code != 200:
        return Response({'error': 'Failed to fetch user info'}, status=status.HTTP_400_BAD_REQUEST)

    userinfo = userinfo_response.json()
    email = userinfo.get('email')
    name = userinfo.get('name', 'Unknown')
    phone_number = userinfo.get('phone_number', '')

    if email:
        user, created = Customer.objects.get_or_create(email=email, defaults={'name': name, 'phone_number': phone_number})
        if created:
            user.set_unusable_password()  # Prevents password login for OIDC users
            user.save()

        # Log in user
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Ensures authentication works
        django_login(request, user)

        # Generate JWT token for frontend use
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Authentication successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid OpenID response'}, status=status.HTTP_400_BAD_REQUEST)