from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

import utils
from utils import get_track_data_by_url
from web.enums import RoomRole
from web.models import Room, User, PlaylistTrack, Message, BannedUserRoom, UserRoom


class UserSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
        )
        read_only_fields = ("email",)


class UserRoomSerializer(serializers.ModelSerializer):
    room_role = serializers.SerializerMethodField(method_name="get_room_role")

    class Meta:
        model = User
        fields = ["id", "email", "room_role", "name"]

    def get_room_role(self, obj):
        return obj.userroom_set.filter(room=self.context["room"]).first().room_role


class MessageSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "text", "created_at", "user_id")


class PlaylistTrackSerializer(NestedHyperlinkedModelSerializer):
    def validate(self, attrs):
        data = get_track_data_by_url(attrs.get("link", None))
        if not data["title"] or not data["thumbnail_url"]:
            raise serializers.ValidationError("Wrong YT link!")
        attrs.update(
            {
                "title": data["title"],
                "order_num": self.context["order_num"],
                "thumbnail_url": data["thumbnail_url"],
                "room_id": self.context["room"].id,
            }
        )
        return attrs

    class Meta:
        model = PlaylistTrack
        fields = (
            "id",
            "title",
            "link",
            "thumbnail_url",
            "order_num",
        )
        read_only_fields = (
            "id",
            "title",
            "thumbnail_url",
            "order_num",
        )


class RoomSerializer(NestedHyperlinkedModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    playlist = PlaylistTrackSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            attrs["users"] = Room.users
            attrs["playlist"] = Room.playlist
            attrs["messages"] = Room.messages
        if not attrs.get("code", None):
            attrs["code"] = utils.create_room_code()
        return attrs

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "code",
            "users",
            "playlist",
            "created_at",
            "privacy",
            "messages",
        )
        read_only_fields = ("code",)


class RoomRetrieveSerializer(RoomSerializer):
    users = UserRoomSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["users"].context.update(self.context)


class RoomBriefSerializer(NestedHyperlinkedModelSerializer):
    listener_amount = serializers.IntegerField(source="users.count")

    class Meta:
        model = Room
        fields = ("id", "name", "privacy", "listener_amount")
        read_only_fields = fields


class BannedUserSerializer(NestedHyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BannedUserRoom
        fields = ("user", "banned_at", "banned_until", "ban_type")
        read_only_fields = fields


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class TrackSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    track_url = serializers.URLField()
    thumbnail_url = serializers.URLField()
    duration = serializers.CharField(max_length=10)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
        )


class RoomRoleSerializer(serializers.Serializer):
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, obj):
        return obj[0]

    def get_label(self, obj):
        return obj[1]


class RoomRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoom
        fields = ["room_role", "user"]
