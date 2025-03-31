# customer/urls.py
from django.urls import path
from .views.register_views import register_user
from .views.login_views import login_user
from .views.oidc_views import oidc_login,oidc_callback
from .views.success_views import success
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    
    
    path('oidc/login/', oidc_login, name='oidc_login'),
    path('oidc/callback/', oidc_callback, name='oidc_callback'),
    path('success/', success, name='success'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]