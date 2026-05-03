from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.customer_viewset import CustomerViewSet
from .views.oidc_views import oidc_login, oidc_callback
from .views.success_views import success

router = SimpleRouter()
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = router.urls + [
    path('oidc/login/', oidc_login, name='oidc_login'),
    path('oidc/callback/', oidc_callback, name='oidc_callback'),
    path('success/', success, name='success'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
