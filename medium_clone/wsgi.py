"""
WSGI config for medium_clone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""



import sys

print("==> Starting WSGI...", file=sys.stderr)

from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
except Exception as e:
    print("WSGI error:", str(e), file=sys.stderr)
    raise
