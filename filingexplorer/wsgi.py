"""
WSGI config for filingexplorer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
from wsgi_sslify import sslify

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filingexplorer.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

if not bool(os.environ.get('DJANGO_DEVELOPMENT')):
    application = sslify(application, subdomains=True)
