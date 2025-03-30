from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ju(nyql!isq_vo7@_1#jh_z$os6(i%lz)01-vbeq@*&9vt0%x2'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Configure Django sites framework
SITE_ID = 1
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']
AUTH_USER_MODEL = 'customer_service.Customer'
REST_AUTH_TOKEN_MODEL = 'account_service.Token'

#Afrca Talking sms gateway
AFRICASTALKING_USERNAME = 'sandbox'
AFRICASTALKING_API_KEY = 'atsk_878fed6f26cb4e196ab242bd5a6df11dc8afee70f2b4dfdd3a925c282ad9f76c6c99a1fc'
AFRICASTALKING_API_URL = 'https://api.sandbox.africastalking.com/version1/messaging'

# OIDC configuration
OIDC_RP_CLIENT_ID = '638828902981-jst85g7pdgng9rpi2fqg2su0pg1ph526.apps.googleusercontent.com'
OIDC_RP_CLIENT_SECRET = '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'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
OIDC_OP_TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
OIDC_OP_USERINFO_ENDPOINT = 'https://openidconnect.googleapis.com/v1/userinfo'
OIDC_OP_JWKS_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/certs'

LOGIN_REDIRECT_URL = 'http://localhost:8000/api/ecommerce/account/oidc/callback/'
LOGOUT_REDIRECT_URL = '/'  # Redirect after logout

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '9047-102-215-40-130.ngrok-free.app'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

     # OpenID Connect provider config
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',

    'rest_framework',
    'rest_framework.authtoken',

    # modules
    'order_service',
    'customer_service',
    'account_service',
    'oauth2_provider',
]

# Token Authentication settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
       # 'rest_framework.authentication.SessionAuthentication',
       # 'rest_framework.authentication.BasicAuthentication',
       # 'rest_framework.authentication.TokenAuthentication',
       'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTHENTICATION_BACKENDS = [
    'account_service.custom_auth_backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

LOGIN_URL = '/admin/login/'

# Required for `allauth`
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Skip email verification for simplicity
ACCOUNT_EMAIL_REQUIRED = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

ROOT_URLCONF = 'ecommerce_rest_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_rest_api.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'postgres',
        'PASSWORD': 'java',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization and localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'