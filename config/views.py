# config/views.py
from django.shortcuts import redirect


def homepage(request):
    return redirect("admin:index") 