import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.tests.factories import UserFactory, RoomFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def room():
    return RoomFactory()


def test_status(api_client):
    response = api_client.get(reverse("status"))
    print(response)
    assert response.status_code == status.HTTP_200_OK


def test_room_unauthorized(api_client, room, user):
    api_client.force_login(user)
    response = api_client.get(reverse("room-detail", args=(room.id,)))
    assert response.status_code == status.HTTP_404_NOT_FOUND
