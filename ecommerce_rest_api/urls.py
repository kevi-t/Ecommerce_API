# ecommerce_rest_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ecommerce/customer/', include('customer_service.urls')),
    path('api/ecommerce/order/', include('order_service.urls')),
    path('api/ecommerce/account/', include('account_service.urls')),
    path('accounts/', include('allauth.urls')),
]