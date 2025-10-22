"""
WSGI config for delivery_ms project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_ms.settings')

application = get_wsgi_application()
