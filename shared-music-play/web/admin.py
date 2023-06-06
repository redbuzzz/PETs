from django.contrib import admin

from web.models import User, Room, Message, BannedUserRoom


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ["email", "role", "name"]
    list_display = ["email", "role", "name"]
    search_fields = ["email"]
    list_filter = ["role"]


@admin.register(Room)
class BookAdmin(admin.ModelAdmin):
    fields = ["name", "created_at", "privacy"]
    list_display = ["name", "created_at", "privacy"]
    search_fields = ["name"]
    list_filter = ["privacy"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ["user", "room", "text"]
    list_display = ["user", "room", "text"]
    list_filter = ["user"]


@admin.register(BannedUserRoom)
class BannedUserRoomAdmin(admin.ModelAdmin):
    fields = ["user", "room", "banned_at", "banned_until", "ban_type"]
    list_display = ["user", "room", "banned_at", "banned_until", "ban_type"]
    search_fields = ["room"]
    list_filter = ["ban_type", "room", "user"]
