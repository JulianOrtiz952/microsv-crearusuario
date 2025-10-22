"""
WSGI config for customers_ms project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'customers_ms.settings')

application = get_wsgi_application()
