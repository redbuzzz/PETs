from datetime import date

from django.contrib.auth import authenticate
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets, serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.serializers import (
    RoomSerializer,
    PlaylistTrackSerializer,
    MessageSerializer,
    BannedUserSerializer,
    TokenResponseSerializer,
    ProfileSerializer,
    UserRoomSerializer,
    RoomRoleUpdateSerializer,
    RoomRoleSerializer,
    RoomRetrieveSerializer,
)
from utils import get_list_track_by_search
from web.enums import RoomRole
from web.models import Room, UserRoom, BannedUserRoom, User
from .serializers import RegistrationSerializer, LoginSerializer, RoomBriefSerializer, TrackSerializer


# /rooms
class RoomViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.action == "public":
            return Room.objects.filter(privacy="public").exclude(users=self.request.user)
        if self.action == "retrieve":
            return Room.objects.filter(Q(users=self.request.user) | Q(privacy="public")).distinct()
        return self.request.user.rooms

    def get_serializer_class(self):
        if self.action == "list" or self.action == "public":
            return RoomBriefSerializer
        elif self.action == "roles":
            return RoomRoleSerializer
        elif self.action == "create":
            return RoomSerializer
        elif self.action == "retrieve":
            return RoomRetrieveSerializer
        return RoomSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "retrieve":
            room = self.get_object()
            context.update({"room": room})
        return context

    @action(methods=["POST"], detail=False)
    def join(self, request):
        code = request.data["code"]
        user = request.user

        room = get_object_or_404(Room, code=code)

        if room.users.contains(user):
            return Response({"detail": "Already joined a room."}, status=status.HTTP_409_CONFLICT)

        if BannedUserRoom.objects.filter(
            Q(user=user), Q(room=room), Q(banned_until__gte=date.today()) | Q(banned_until__isnull=True)
        ).exists():
            return Response({"detail": "Sorry, you are banned in this room."}, status=status.HTTP_403_FORBIDDEN)

        room.users.add(user, through_defaults={})
        serializer = RoomBriefSerializer(room, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room_data = serializer.validated_data
        self.perform_create(serializer)
        UserRoom.objects.create(
            room_role=RoomRole.admin, user_id=request.user.id, room_id=Room.objects.filter(**room_data).first().id
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["GET"], detail=False)
    def roles(self, request):
        roles = RoomRole.choices
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def public(self, request):
        return self.list(request)


# /rooms/<room_id>
class RoomNestedViewSet(GenericViewSet):
    def get_room(self):
        return get_object_or_404(Room, id=self.kwargs["rooms_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"room": RoomNestedViewSet.get_room(self=self)})
        return context


# /rooms/<room_id>/playlist
class RoomPlaylistViewSet(RoomNestedViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = PlaylistTrackSerializer

    def get_queryset(self):
        return super().get_room().playlist

    def get_serializer_context(self):
        context = super().get_serializer_context()
        max_order_num = context["room"].playlist.last()
        order_num = max_order_num.order_num + 1 if max_order_num else 0
        context.update({"order_num": order_num})
        return context


# /rooms/<room_id>/messages
class RoomMessagesViewSet(RoomNestedViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return super().get_room().messages


# /rooms/<room_id>/banned_users
class RoomBannedUsersViewSet(RoomNestedViewSet, mixins.ListModelMixin):
    serializer_class = BannedUserSerializer

    def get_queryset(self):
        return BannedUserRoom.objects.filter(room_id=self.get_room().id).prefetch_related("user")


@api_view(["GET"])
@permission_classes([])
def status_view(request):
    return Response({"status": "OK"})


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get("user", {}))
        if not serializer.is_valid():
            return Response({"detail": "Validation error", **serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token = Token.objects.create(user=user)
        response_data = {"token": token.key}
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get("user", {}))
        if not serializer.is_valid():
            return Response({"detail": "Validation error", **serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(**serializer.validated_data)
        if user is None:
            raise AuthenticationFailed(detail="Wrong email or password")
        token, created = Token.objects.get_or_create(user=user)
        response_data = {"token": token.key}
        response_serializer = TokenResponseSerializer(response_data)
        return Response(response_serializer.data)


@api_view(["GET"])
@permission_classes([])
def search_tracks(request):
    search_query = request.GET.get("search_text", "")
    track_list = get_list_track_by_search(search_query)
    serializer = TrackSerializer(track_list, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["PUT", "GET"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = ProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if request.method == "PUT":
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class RoomUsersViewSet(RoomNestedViewSet, mixins.ListModelMixin):
    serializer_class = UserRoomSerializer

    def get_queryset(self):
        room = self.get_room()
        users = User.objects.filter(userroom__room=room).prefetch_related(
            Prefetch("userroom_set", queryset=UserRoom.objects.filter(room=room))
        )
        return users
