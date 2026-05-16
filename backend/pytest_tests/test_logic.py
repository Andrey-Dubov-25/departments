from http import HTTPStatus

from django.urls import reverse
from pytest_lazy_fixtures import lf
import pytest


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'data, status',
    (
        (lf('department_child_data'), HTTPStatus.CREATED),
        (lf('department_child_bad_data'), HTTPStatus.BAD_REQUEST)
    )
)
def test_create_department(client, department_parent, data, status):
    """Тестирование создания подразделения."""

    url = reverse('api:departments-list')
    response = client.post(url, data)
    assert response.status_code == status


@pytest.mark.parametrize(
    'data, status',
    (
        (lf('employees_data'), HTTPStatus.CREATED),
        (lf('employees_bad_data'), HTTPStatus.BAD_REQUEST)
    )
)
def test_create_employees(client, department_parent, data, status):
    """Тестирование создания сотрудника."""

    url = reverse('api:departments-employees', args=(department_parent.pk,))
    response = client.post(url, data)
    assert response.status_code == status
