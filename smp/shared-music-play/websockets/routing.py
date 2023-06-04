from django.urls import path

from websockets.consumers import RoomConsumer

websocket_urlpatterns = [path("ws/room/<int:room_id>", RoomConsumer.as_asgi())]
