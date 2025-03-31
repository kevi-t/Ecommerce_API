#orders/urls.py
from django.urls import path
from .views import views
from .views.list_views import get_customer_orders

urlpatterns = [
    path('place-order/', views.create_order, name='create_order'),
    path('list/', get_customer_orders, name='customer-orders'),
]