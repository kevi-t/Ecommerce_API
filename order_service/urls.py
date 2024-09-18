from django.urls import path
from .import views

urlpatterns = [
    path('place-order/', views.create_order, name='create_order'),
]