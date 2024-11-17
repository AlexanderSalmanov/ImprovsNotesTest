import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from notes.models import Notes
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(user, redis_client):
    client = APIClient()
    refresh_token = RefreshToken.for_user(user)
    access_token = str(refresh_token.access_token)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    redis_client.set(f'jwt:{access_token}', '', ex=60*60)

    return client


@pytest.fixture
def note(user):
    return Notes.objects.create(title='Test Note', content='Test content', created_by=user)
