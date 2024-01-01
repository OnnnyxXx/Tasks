import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import user_messeges.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coolsite.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            user_messeges.routing.websocket_urlpatterns
        )
    ),
})