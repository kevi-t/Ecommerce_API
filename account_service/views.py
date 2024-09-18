import requests
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from customer_service.models import Customer

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Debugging: Check if request data is received properly
    print(f"Login attempt - Email: {email}, Password: {password}")

    # Authenticate user
    user = authenticate(email=email, password=password)
    if user is not None:
        # Generate or retrieve authentication token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

def login_callback(request):
    # Logic for login callback, you can handle OAuth success or failure here
    return HttpResponse("Login successful")

@csrf_exempt
def oauth_callback(request):
    # Handle the callback from the provider, extract code and exchange for an access token
    code = request.GET.get('code')
    if not code:
        return HttpResponse("No code provided", status=400)

    # Exchange authorization code for access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': '638828902981-jst85g7pdgng9rpi2fqg2su0pg1ph526.apps.googleusercontent.com',  # Replace with actual client_id
        'client_secret': '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',  # Replace with actual client_secret
        'redirect_uri': 'http://127.0.0.1:8000/api/ecommerce/account/login/callback/',
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()

    if 'access_token' in token_data:
        # Use access token to get user information
        access_token = token_data['access_token']
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo = userinfo_response.json()

        # Here, you'd handle user login or creation logic based on userinfo
        # For simplicity, we'll just redirect to a success page
        return redirect('/api/ecommerce/account/success/')
    else:
        # If token exchange fails
        return HttpResponse("Error during token exchange", status=400)

def success(request):
    # Success page after Google OAuth login
    return HttpResponse("Authentication via Google OpenID was successful!")