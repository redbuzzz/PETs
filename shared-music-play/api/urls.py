from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from api.views import (
    RoomViewSet,
    status_view,
    RoomPlaylistViewSet,
    RoomBannedUsersViewSet,
    RoomMessagesViewSet,
    RegistrationAPIView,
    LoginAPIView,
    search_tracks,
    update_profile,
    RoomUsersViewSet,
)

room_router = SimpleRouter()
room_router.register("rooms", RoomViewSet, basename="rooms")

room_nested_router = routers.NestedSimpleRouter(room_router, "rooms", lookup="rooms")
room_nested_router.register("playlist", RoomPlaylistViewSet, basename="playlist")
room_nested_router.register("banned_users", RoomBannedUsersViewSet, basename="banned_users")
room_nested_router.register("messages", RoomMessagesViewSet, basename="messages")
room_nested_router.register("users", RoomUsersViewSet, basename="users")

urlpatterns = (
    [
        path("status", status_view, name="status"),
        path("registr", RegistrationAPIView.as_view()),
        path("login", LoginAPIView.as_view()),
        path("search", search_tracks, name="search"),
        path("profile", update_profile),
    ]
    + room_router.urls
    + room_nested_router.urls
)
