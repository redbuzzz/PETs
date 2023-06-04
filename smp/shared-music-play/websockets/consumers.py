import json
from pprint import pprint

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Prefetch
from rest_framework.authtoken.models import Token

from api.serializers import PlaylistTrackSerializer
from utils import get_track_data_by_url
from web.models import Room, PlaylistTrack, Message, UserRoom


class RoomConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_room = None
        self.group_name = None
        self.user = None
        self.room = None

    async def connect(self):
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = "room_%s" % room_id

        self.user = self.scope["user"]
        if self.user.is_anonymous:
            return await self.disconnect(401)

        self.room = await Room.objects.filter(id=room_id, users=self.user).afirst()
        if self.room is None:
            return await self.disconnect(404)

        self.user_room = await UserRoom.objects.filter(room=self.room, user=self.user).afirst()

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def add_message_to_db(self, message):
        Message.objects.create(**{"user_id": self.user.id, "room_id": self.room.id, "text": message.get("text", "")})

    @database_sync_to_async
    def create_track(self, link):
        track_data = get_track_data_by_url(link)
        last_track = self.room.playlist.last()
        order_num = last_track.order_num + 1 if last_track else 0
        return PlaylistTrack.objects.create(
            title=track_data["title"],
            link=link,
            order_num=order_num,
            thumbnail_url=track_data["thumbnail_url"],
            room_id=self.room.id,
        )

    @database_sync_to_async
    def refresh_from_db(self):
        self.user.refresh_from_db()
        self.room.refresh_from_db()
        self.user_room.refresh_from_db()

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        print("message")
        pprint(message, indent=4)

        message_type = message.get("type", None)
        data = message.get("data", None)
        if not message_type:
            return

        print("RECEIVING", message)
        await self.refresh_from_db()
        await getattr(self, message_type)(message, data)

    async def player_request(self, message, data):
        await self.channel_layer.group_send(
            self.group_name, {"type": "broadcast_without_sender", "message": message, "sender": self.user.id}
        )

    async def player_init(self, message, data):
        await self.channel_layer.group_send(
            self.group_name, {"type": "broadcast_without_sender", "message": message, "sender": self.user.id}
        )

    async def player(self, message, data):
        await self.channel_layer.group_send(
            self.group_name, {"type": "broadcast_without_sender", "message": message, "sender": self.user.id}
        )

    async def chat(self, message, data):
        await self.add_message_to_db(data)
        message["data"]["username"] = self.user.name
        await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": message})

    async def playlist_order(self, message, data):
        new_order = data.get("playlist")
        original_playlist = await database_sync_to_async(list)(self.room.playlist)
        original_order = await database_sync_to_async(list)(self.room.playlist.values_list("id", flat=True))

        if sorted(new_order) != sorted(original_order):
            message.data.playlist = original_order
            await self.send(text_data=json.dumps(message))
            return

        for i in range(len(original_order)):
            track = original_playlist[i]
            track.order_num = new_order.index(track.id)

        await PlaylistTrack.objects.abulk_update(original_playlist, ['order_num'])

        await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": message})

    async def add_track(self, message, data):
        link = data.get("link", None)
        track = await self.create_track(link)
        new_message = {"type": "add_track", "data": {"track": PlaylistTrackSerializer(track).data}}
        await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": new_message})

    async def delete_track(self, message, data):
        track_id = data.get("id")
        await PlaylistTrack.objects.filter(room=self.room, id=track_id).adelete()
        await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": message})

    async def clear_playlist(self, message, data):
        await PlaylistTrack.objects.filter(room=self.room).adelete()
        await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": message})

    async def update_room_role(self, message, data):
        if self.user_room.room_role == "admin":
            room_role = data.get("room_role", None)
            user_id = data.get("user_id", None)
            await UserRoom.objects.filter(user_id=user_id, room=self.room).aupdate(room_role=room_role)
            await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": message})

    # Receive message from room group
    async def broadcast_without_sender(self, event):
        message = event["message"]
        sender = event["sender"]
        print("SENDING:", message)
        # Send message to WebSocket
        if self.user and self.user.id != sender:
            await self.send(text_data=json.dumps(message))

    async def broadcast(self, event):
        message = event["message"]
        print("SENDING:", message)
        await self.send(text_data=json.dumps(message))
