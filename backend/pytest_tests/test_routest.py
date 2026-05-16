from http import HTTPStatus

from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_departments(client):
    """Тестирование доступности страницы подразделений."""
    url = reverse('api:departments-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
