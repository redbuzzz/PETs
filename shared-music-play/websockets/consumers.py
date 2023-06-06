import json
from datetime import date
from pprint import pprint

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Prefetch, Q
from rest_framework.authtoken.models import Token

from api.serializers import PlaylistTrackSerializer, UserRoomSerializer
from utils import get_track_data_by_url
from web.models import Room, PlaylistTrack, Message, UserRoom, User, BannedUserRoom


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

        self.room = await Room.objects.aget(id=room_id)

        self.user_room = await UserRoom.objects.filter(room=self.room, user=self.user).afirst()

        if not self.user_room:
            if self.room.privacy != "public":
                return await self.disconnect(404)
            if not await self.add_user_to_room():
                return await self.disconnect(403)
            self.user_room = await UserRoom.objects.filter(room=self.room, user=self.user).afirst()

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "broadcast", "message": await self.create_greeting_message(), "sender": self.user.id},
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def add_message_to_db(self, message):
        Message.objects.create(**{"user_id": self.user.id, "room_id": self.room.id, "text": message.get("text", "")})

    @database_sync_to_async
    def add_user_to_room(self):
        if BannedUserRoom.objects.filter(
            Q(user=self.user), Q(room=self.room), Q(banned_until__gte=date.today()) | Q(banned_until__isnull=True)
        ).exists():
            return False
        self.room.users.add(self.user, through_defaults={})
        return True

    @database_sync_to_async
    def create_greeting_message(self):
        return {
            "type": "user",
            "data": {
                "user": {
                    "id": self.user.id,
                    "email": self.user.email,
                    "name": self.user.name,
                    "room_role": self.user_room.room_role,
                }
            },
        }

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
    def ban_user(self, user_id, ban_until):
        if self.user_room.room_role == "user":
            return False
        user = User.objects.get(id=user_id)
        room_role = user.userroom_set.get(room=self.room).room_role

        if room_role == "admin" or (room_role == "moderator" and self.user_room.room_role == "moderator"):
            return False

        self.room.users.remove(user)
        self.room.banned_users.remove(user)
        BannedUserRoom.objects.create(user=user, room=self.room, banned_until=ban_until)
        return True

    @database_sync_to_async
    def refresh_from_db(self):
        self.user.refresh_from_db()
        self.room.refresh_from_db()
        self.user_room.refresh_from_db()

    @database_sync_to_async
    def unban_user(self, user_id):
        if self.user_room.room_role == "user":
            return False
        self.room.banned_users.remove(User.objects.get(id=user_id))
        return True

    @database_sync_to_async
    def delete_active_room(self):
        if self.user_room.room_role != "admin":
            return False
        self.room.delete()
        return True

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

        method = None
        try:
            method = getattr(self, message_type)
        except AttributeError:
            print("Message type not found", message_type)

        if method is not None:
            await method(message, data)

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

        await PlaylistTrack.objects.abulk_update(original_playlist, ["order_num"])

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

    async def ban(self, message, data):
        if await self.ban_user(data["user_id"], data.get("ban_until", None)):
            await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": message})

    async def unban(self, message, data):
        if await self.unban_user(data["user_id"]):
            await self.channel_layer.group_send(self.group_name, {"type": "broadcast", "message": message})

    async def delete_room(self, message, data):
        if await self.delete_active_room():
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
