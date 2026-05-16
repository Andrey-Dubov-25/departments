import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_department_in_list(client, department_parent):
    """Тестирование наличия данных подразделения в запросе к подразделению."""
    url = reverse('api:departments-list')
    response = client.get(url)
    quest_data = response.data[0]
    assert (department_parent.name == quest_data['name']) is True
