# your_project/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from myblog.routing import application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Application is both ASGI and HTTP
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": application,
})
