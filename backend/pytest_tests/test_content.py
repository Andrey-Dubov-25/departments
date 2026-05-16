from django.urls import reverse
# from pytest_lazy_fixtures import lf
import pytest


pytestmark = pytest.mark.django_db


def test_department_in_list(client, department_parent):
    """Тестирование наличие квеста в запросе к странице квестов."""
    url = reverse('api:departments-list')
    response = client.get(url)
    quest_data = response.data[0]
    assert (department_parent.name == quest_data['name']) is True
