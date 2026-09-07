import os
import sys
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
app = application

try:
    from django.core.management import call_command
    call_command('migrate', '--noinput', verbosity=0)
except Exception as e:
    print(f'Migration error on startup: {e}', file=sys.stderr)