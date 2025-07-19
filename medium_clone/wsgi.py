"""
WSGI config for medium_clone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import sys
import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medium_clone.settings')


try:
    application = get_wsgi_application()
except Exception as e:
    print("❌ Error during WSGI startup:", str(e), file=sys.stderr)
    raise

