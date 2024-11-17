import pytest

from django.urls import reverse
from django.core.cache import cache
from rest_framework import status


@pytest.mark.django_db
def test_create_note(authenticated_api_client, user, note):
    url = reverse('notes:list-create')
    payload = {
        'title': 'New Title',
        'content': 'New Content'
    }
    cache_key = f'test_cache_key_user_{user.id}'
    cache.set(cache_key, note, 60 * 15)
    
    assert cache.get(cache_key) is not None
    cache.delete(cache_key)
    
    response = authenticated_api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == payload['title']
    assert response.data['content'] == payload['content']
    
    assert not cache.get(cache_key)
    
@pytest.mark.django_db
def test_get_notes(authenticated_api_client):
    url = reverse('notes:list-create')
    response = authenticated_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    
    
@pytest.mark.django_db
def test_unauthorized_get_notes(api_client):
    url = reverse('notes:list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
@pytest.mark.django_db
def test_delete_note(authenticated_api_client, user, note):
    cache_key = f'test_cache_key_user_{user.id}'
    cache.set(cache_key, note, 60 * 15)
    
    assert cache.get(cache_key) is not None
    
    url = reverse('notes:update-delete', kwargs={'id': note.id})
    response = authenticated_api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    cache.delete(cache_key)
    assert not cache.get(cache_key)
    
    
@pytest.mark.django_db
def test_update_note(authenticated_api_client, user, note):
    cache_key = f'test_cache_key_user_{user.id}'
    cache.set(cache_key, note, 60 * 15)
    old_title = note.title
    
    assert cache.get(cache_key) is not None
    assert old_title == 'Test Note'
    
    payload = {'title': 'New Note Title'}
    
    url = reverse('notes:update-delete', kwargs={'id': note.id})
    response = authenticated_api_client.patch(url, payload, format='json')
    cache.delete(cache_key)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == payload['title']
    assert response.data['title'] != old_title
    assert not cache.get(cache_key)
    
    
    
