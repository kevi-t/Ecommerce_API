# customer/views.py
from django.http import JsonResponse
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.tokens import RefreshToken


# ✅ Success Page
@login_required
def success(request):
    user = request.user
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })
    # return HttpResponse("Authentication was successful!")