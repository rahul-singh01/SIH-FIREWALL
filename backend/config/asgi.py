import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Get the ASGI application for the Django project.
application = get_asgi_application()
