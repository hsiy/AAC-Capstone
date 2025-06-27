"""
WSGI config for AACForm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.db import connections
from django.db.utils import OperationalError
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AACForm.settings')

try:
    # Attempt to get a cursor to test the DB connection
    connections['default'].cursor()
except OperationalError:
    print("Database connection failed. Exiting Application.")
    sys.exit(1)

application = get_wsgi_application()
