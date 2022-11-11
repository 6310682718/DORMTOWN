import os

from django.core.wsgi import get_wsgi_application


import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dormtown.settings')

application = get_wsgi_application()