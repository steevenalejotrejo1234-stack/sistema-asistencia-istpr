"""
WSGI config for instituto_recuay project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instituto_recuay.settings')

application = get_wsgi_application()
