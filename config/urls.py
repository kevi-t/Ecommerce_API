from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from .views import homepage


urlpatterns = [
    path("", homepage, name="home"),
    path('admin/', admin.site.urls),
    path('api/ecommerce/customer/', include('customer.urls')),
    path('api/ecommerce/order/', include('orders.urls')),
    path('accounts/', include('allauth.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('o/', include(oauth2_urls)),
]