from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from user_messeges.consumers import ChatConsumer

websocket_urlpatterns = [
    path('messages/<int:room_id>/', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})