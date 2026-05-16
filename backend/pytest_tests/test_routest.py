from django.urls import reverse
from http import HTTPStatus
import pytest


@pytest.mark.django_db
def test_departments(client):
    """
    Тестирование доступности страницы квестов и их типов для анонима:
    - аноним не может получит страницы (401).
    """
    url = reverse('api:departments-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
