"""
WSGI config for django_dynamic_url project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_dynamic_url.settings')
config('EMAIL_HOST_USER')
config('EMAIL_HOST_PASSWORD')
application = get_wsgi_application()
