from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('oidc/login/', views.oidc_login, name='oidc_login'),
    path('oidc/callback/', views.oidc_callback, name='oidc_callback'),
    path('success/', views.success, name='success'),


    # path('login/callback/', views.oauth_callback, name='oauth_callback'),
    # path('login/callback1/', views.login_callback, name='login_callback'),

]