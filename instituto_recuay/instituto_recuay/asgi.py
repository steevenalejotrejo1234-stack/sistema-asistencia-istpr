"""
ASGI config for instituto_recuay project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instituto_recuay.settings')

application = get_asgi_application()
