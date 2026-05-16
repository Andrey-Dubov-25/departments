import pytest
# from rest_framework.test import APIClient

from departments.models import Department


@pytest.fixture
def department_parent_data():
    data = {
        'name': 'Тестовое подразделение'
    }
    return data


@pytest.fixture
def department_parent(department_parent_data):
    department = Department.objects.create(**department_parent_data)
    return department


@pytest.fixture
def department_child_data(department_parent):
    data = {
        'name': 'Второе тестовое подразделение',
        'parent': department_parent.id
    }
    return data


@pytest.fixture
def department_child_bad_data(department_parent):
    data = {
        'name': '',
        'parent': department_parent.id
    }
    return data


@pytest.fixture
def department_child(department_child_data):
    department = Department.objects.create(**department_child_data)
    return department


@pytest.fixture
def department_child_for_child_data(department_child):
    data = {
        'name': 'Третье тестовое подразделение',
        'parent': department_child.id
    }
    return data


@pytest.fixture
def department_child_for_child(department_child_for_child_data):
    department = Department.objects.create(**department_child_for_child_data)
    return department


@pytest.fixture
def employees_data():
    data = {
        'full_name': 'Тестовый сотрудник',
        'position': 'Тестовая должность'
    }
    return data


@pytest.fixture
def employees_bad_data():
    data = {
        'full_name': '',
        'position': 'Тестовая должность'
    }
    return data
