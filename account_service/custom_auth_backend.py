from django.contrib.auth.backends import BaseBackend
from customer_service.models import Customer

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Customer.objects.get(email=email)
            if user.check_password(password):
                return user
        except Customer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None