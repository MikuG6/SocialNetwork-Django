import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('token_obtain')
    response = api_client.post(url, data={'username': "test", 'password': "te5st"})
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_request(api_client):
    url = reverse('token_obtain')
    response = api_client.post(url, data={'username': "test", 'password': "test"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthorized_request2(api_client, auth_bearer_token):
    url = reverse('service:self_profile')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_bearer_token)
    response = api_client.get(url)
    assert response.status_code == 2001
