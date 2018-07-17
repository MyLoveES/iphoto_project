"""
WSGI config for iphoto_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iphoto_project.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'iphoto_project.settings'
os.environ["CELERY_LOADER"] = "django"
application = get_wsgi_application()
