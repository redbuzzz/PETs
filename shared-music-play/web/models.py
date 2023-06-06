from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db.models import Prefetch

from web.enums import Role, RoomPrivacy, RoomRole, BanType


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, commit=True, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, role=Role.admin, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True)
    role = models.CharField(choices=Role.choices, max_length=15, default=Role.user)
    name = models.CharField(max_length=255, null=False, blank=False)

    @property
    def rooms(self):
        return Room.objects.filter(userroom__user_id=self.id)

    @property
    def is_staff(self):
        return self.role in (Role.admin, Role.staff)

    @property
    def is_superuser(self):
        return self.role == Role.admin

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=2)
        token = jwt.encode({"id": self.pk, "exp": int(dt.strftime("%s"))}, settings.SECRET_KEY, algorithm="HS256")

        return token

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"User[email: {self.email}]"


class Room(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(choices=RoomPrivacy.choices, max_length=15, default=RoomPrivacy.private)
    code = models.CharField(max_length=5, null=True, blank=True, unique=True)
    users = models.ManyToManyField(User, through="UserRoom", related_name="users")
    banned_users = models.ManyToManyField(User, through="BannedUserRoom", related_name="banned_users")

    @property
    def playlist(self):
        return PlaylistTrack.objects.filter(room_id=self.id).order_by("order_num")

    @property
    def messages(self):
        return Message.objects.filter(room_id=self.id).order_by("created_at")


class UserRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_role = models.CharField(choices=RoomRole.choices, max_length=15, default=RoomRole.user)
    joined_at = models.DateTimeField(auto_now_add=True)


class FavoriteSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=255, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)


class Message(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()


class BannedUserRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    banned_at = models.DateTimeField(auto_now_add=True)
    banned_until = models.DateTimeField(null=True)
    ban_type = models.CharField(choices=BanType.choices, max_length=15, default=BanType.room)


class TrackHistory(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    link = models.CharField(max_length=255, null=True, blank=True)
    listened_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)


class PlaylistTrack(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=False)
    thumbnail_url = models.CharField(max_length=255)
    order_num = models.IntegerField()

    class Meta:
        ordering = ["order_num"]
