"""
ASGI config for shared_music_play project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from websockets.middleware import TokenAuthMiddleware
from websockets.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shared_music_play.settings")

# TODO: add AllowedHostsOriginValidator
application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": TokenAuthMiddleware(URLRouter(websocket_urlpatterns))}
)
