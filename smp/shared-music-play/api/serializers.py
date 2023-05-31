from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

import utils
from utils import get_track_data_by_url
from web.models import Room, User, PlaylistTrack, Message, BannedUserRoom


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
        )
        read_only_fields = ("email",)


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

    def validate(self, attrs):
        if self.context["request"].method != "POST":
            attrs["users"] = Room.users
            attrs["playlist"] = Room.playlist
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
        )
        read_only_fields = ("code",)


class RoomBriefSerializer(NestedHyperlinkedModelSerializer):
    listener_amount = serializers.IntegerField(source="users.count")

    class Meta:
        model = Room
        fields = ("id", "name", "privacy", "listener_amount")
        read_only_fields = fields


class MessageSerializer(NestedHyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        attrs.update({"room_id": self.context["room"].id, "user_id": self.context["request"].user.id})
        return attrs

    class Meta:
        model = Message
        fields = ("id", "user", "text", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


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
