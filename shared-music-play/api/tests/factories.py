import factory

from web.models import User, Room


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")

    class Meta:
        model = User


class RoomFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Room
