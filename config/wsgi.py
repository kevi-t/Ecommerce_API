"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# get_wsgi_application() must run first — it initialises the app registry.
# Migrations are safe to run after that; Django skips already-applied ones.
application = get_wsgi_application()
app = application

try:
    from django.core.management import call_command
    call_command('migrate', '--noinput', verbosity=0)
except Exception as e:
    print(f'Migration error on startup: {e}', file=sys.stderr)