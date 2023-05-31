from django.db import models


class Role(models.TextChoices):
    admin = "admin", "Администратор"
    staff = "staff", "Сотрудник"
    user = "user", "Пользователь"


class RoomPrivacy(models.TextChoices):
    private = "private", "Приватная"
    public = "public", "Публичная"


class RoomRole(models.TextChoices):
    admin = "admin", "Администратор"
    moderator = "moderator", "Модератор"
    user = "user", "Пользователь"


class BanType(models.TextChoices):
    room = "room", "Бан в комнате"
    chat = "chat", "Бан в чате"
