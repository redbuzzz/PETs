from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
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
)
from utils import get_list_track_by_search
from web.enums import RoomRole
from web.models import Room, UserRoom, BannedUserRoom, PlaylistTrack
from .serializers import RegistrationSerializer, LoginSerializer, RoomBriefSerializer, TrackSerializer


class RoomViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 5

    serializer_class = RoomSerializer

    def get_queryset(self):
        return self.request.user.rooms

    @action(methods=["get"], detail=False)
    def brief(self, request):
        queryset = self.get_queryset()
        serializer = RoomBriefSerializer(queryset, many=True)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def join(self, request):
        code = request.data["code"]
        user = request.user

        room = get_object_or_404(Room, code=code)

        if room.users.contains(user):
            return Response({"detail": "Already joined a room."}, status=status.HTTP_409_CONFLICT)

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


class RoomNestedViewSet(GenericViewSet):
    def get_room(self):
        return get_object_or_404(Room, id=self.kwargs["rooms_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"room": RoomNestedViewSet.get_room(self=self)})
        return context


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

    @action(methods=["PUT"], detail=False)
    def order(self, request, *args, **kwargs):

        new_order = request.data.get("playlist")
        playlist = self.get_queryset()

        # update ordering, but first check
        original_order = playlist.values_list("id", flat=True)

        if sorted(new_order) != sorted(original_order):
            return Response({"status": "invalid ordering"}, status=status.HTTP_400_BAD_REQUEST)

        # todo optimize (maybe use native queries)
        order = filter(lambda x: x[0] != x[1], zip(range(len(original_order)), new_order, original_order))
        for i in order:
            playlist.filter(id=i[1]).update(order_num=i[0])

        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class RoomMessagesViewSet(RoomNestedViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return super().get_room().messages


class RoomBannedUsersViewSet(RoomNestedViewSet, mixins.ListModelMixin, GenericViewSet):
    serializer_class = BannedUserSerializer

    def get_queryset(self):
        return BannedUserRoom.objects.filter(room_id=self.get_room().id)


@api_view(["GET"])
@permission_classes([])
def status_view(request):
    return Response({"status": "OK"})


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get("user", {}))
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        token = Token.objects.create(user=user)
        response_data = {"token": token.key}
        response_serializer = TokenResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get("user", {}))
        serializer.is_valid(raise_exception=True)
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
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
