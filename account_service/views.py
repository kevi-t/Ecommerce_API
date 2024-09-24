import requests

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from customer_service.models import Customer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login as django_login

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)
    if user is not None:
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),  # Correctly access the access token here
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#
#     print(f"Login attempt - Email: {email}, Password: {password}")
#
#     user = authenticate(email=email, password=password)
#     if user is not None:
#         # return Response({"message": "Login successful"})
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=status.HTTP_200_OK)
#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])
def oidc_login(request):
    # Redirect to the OpenID Connect provider authorization URL
    authorization_url = f"{settings.OIDC_OP_AUTHORIZATION_ENDPOINT}?response_type=code&client_id={settings.OIDC_RP_CLIENT_ID}&redirect_uri={settings.LOGIN_REDIRECT_URL}&scope=openid email"
    return redirect(authorization_url)

@api_view(['GET'])
@permission_classes([AllowAny])
def oidc_callback(request):
    code = request.GET.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.LOGIN_REDIRECT_URL,
        'client_id': settings.OIDC_RP_CLIENT_ID,
        'client_secret': settings.OIDC_RP_CLIENT_SECRET,
    }
    token_response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data=token_data)
    if token_response.status_code != 200:
        return Response({'error': 'Failed to fetch token'}, status=status.HTTP_400_BAD_REQUEST)

    token_response_data = token_response.json()
    access_token = token_response_data.get('access_token')

    userinfo_response = requests.get(settings.OIDC_OP_USERINFO_ENDPOINT, headers={
        'Authorization': f'Bearer {access_token}'
    })
    if userinfo_response.status_code != 200:
        return Response({'error': 'Failed to fetch user info'}, status=status.HTTP_400_BAD_REQUEST)

    userinfo = userinfo_response.json()

    # Authenticate and login the user
    if userinfo.get('email'):
        user, created = Customer.objects.get_or_create(
            email=userinfo['email'],
            defaults={
                'name': userinfo.get('name', ''),
                'phone_number': userinfo.get('phone_number', ''),
                'password': 'temporary_password'  # Handle password appropriately
            }
        )

        # Specify the backend
        user.backend = 'account_service.custom_auth_backend.EmailBackend'  # Adjust if necessary
        django_login(request, user)  # Call the login with the specified backend

        return redirect('success')

    return Response({'error': 'Invalid login'}, status=status.HTTP_400_BAD_REQUEST)

def success(request):
    return HttpResponse("Authentication was successful!")
















# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#
#     print(f"Login attempt - Email: {email}, Password: {password}")
#
#     user = authenticate(email=email, password=password)
#     if user is not None:
#         return Response({"message": "Login successful"})
#         # token, created = Token.objects.get_or_create(user=user)
#         # return Response({'token': token.key}, status=status.HTTP_200_OK)
#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# def login_callback(request):
#     # Logic for login callback, you can handle OAuth success or failure here
#     return HttpResponse("Login successful")
#
# @csrf_exempt
# def oauth_callback(request):
#     # Handle the callback from the provider, extract code and exchange for an access token
#     code = request.GET.get('code')
#     if not code:
#         return HttpResponse("No code provided", status=400)
#     # Exchange authorization code for access token
#     token_url = "https://oauth2.googleapis.com/token"
#     data = {
#         'code': code,
#         'client_id': settings.SOCIALACCOUNT_PROVIDERS['openid_connect']['SERVERS']['google']['client_id'],
#         'client_secret': settings.SOCIALACCOUNT_PROVIDERS['openid_connect']['SERVERS']['google']['secret'],
#         'redirect_uri': settings.SOCIALACCOUNT_PROVIDERS['openid_connect']['SERVERS']['google']['redirect_uri'],
#         'grant_type': 'authorization_code',
#     }
#     response = requests.post(token_url, data=data)
#     token_data = response.json()
#
#     if 'access_token' in token_data:
#         # Use access token to get user information
#         access_token = token_data['access_token']
#         userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
#         headers = {'Authorization': f'Bearer {access_token}'}
#         userinfo_response = requests.get(userinfo_url, headers=headers)
#         userinfo = userinfo_response.json()
#
#         # Here, you'd handle user login or creation logic based on userinfo
#         # For simplicity, we'll just redirect to a success page
#         return redirect('/api/ecommerce/account/success/')
#     else:
#         # If token exchange fails
#         return HttpResponse("Error during token exchange", status=400)
#