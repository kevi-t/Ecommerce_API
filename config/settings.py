from pathlib import Path
from datetime import timedelta
import os
# import dj_database_url
from environ import Env
env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env.bool("DJANGO_DEBUG", default=True)
DEBUG = True

ALLOWED_HOSTS = ['localhost','*']

# Configure Django sites framework
SITE_ID = 1


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    # OpenID Connect provider config
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',

    'rest_framework',
    'rest_framework.authtoken',

    # modules
    'orders',
    'customer',

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
    'customer.authentication.custom_auth_backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]


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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth settingss
AUTH_USER_MODEL = 'customer.Customer'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_VERIFICATION = 'none'  
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = 'http://localhost:8000/api/ecommerce/customer/oidc/callback/'

LOGOUT_REDIRECT_URL = '/' 

REST_AUTH_TOKEN_MODEL = 'customer.Token'

#Afrca Talking sms gateway
AFRICASTALKING_USERNAME = env('AFRICASTALKING_USERNAME')
AFRICASTALKING_API_KEY = env('AFRICASTALKING_API_KEY')
AFRICASTALKING_API_URL = 'https://api.sandbox.africastalking.com/version1/messaging'

# OIDC configuration
OIDC_RP_CLIENT_ID = env('OAUTH_GOOGLE_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = env('OAUTH_GOOGLE_SECRET')
OIDC_OP_AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
OIDC_OP_TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
OIDC_OP_USERINFO_ENDPOINT = 'https://openidconnect.googleapis.com/v1/userinfo'
OIDC_OP_JWKS_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/certs'