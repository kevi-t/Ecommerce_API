from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import OrderViewSet


router = SimpleRouter()
router.register(r'', OrderViewSet, basename='order')

order_place = OrderViewSet.as_view({"post": "create"})
order_list = OrderViewSet.as_view({"get": "list"})

urlpatterns = [
    path('place-order/', order_place, name='order-place-order'),
    path('list/', order_list, name='order-list-legacy'),
] + router.urls
