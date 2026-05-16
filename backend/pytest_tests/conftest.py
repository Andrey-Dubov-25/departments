import pytest

from departments.models import Department


@pytest.fixture
def department_parent_data():
    """Фикстура данных для создания родительского подразделения."""
    data = {
        'name': 'Тестовое подразделение'
    }
    return data


@pytest.fixture
def department_parent(department_parent_data):
    """Фикстура создания родительского подразделения."""
    department = Department.objects.create(**department_parent_data)
    return department


@pytest.fixture
def department_child_data(department_parent):
    """Фикстура данных для создания дочернего подразделения."""
    data = {
        'name': 'Второе тестовое подразделение',
        'parent': department_parent.id
    }
    return data


@pytest.fixture
def department_child_bad_data(department_parent):
    """Фикстура неудачного создания дочернего подразделения."""
    data = {
        'name': '',
        'parent': department_parent.id
    }
    return data


@pytest.fixture
def department_child(department_child_data):
    """Фикстура создания дочернего подразделения."""
    department = Department.objects.create(**department_child_data)
    return department


@pytest.fixture
def department_child_for_child_data(department_child):
    """Фикстура данных для создания поддочернего подразделения."""
    data = {
        'name': 'Третье тестовое подразделение',
        'parent': department_child.id
    }
    return data


@pytest.fixture
def department_child_for_child(department_child_for_child_data):
    """Фикстура создания поддочернего подразделения."""
    department = Department.objects.create(**department_child_for_child_data)
    return department


@pytest.fixture
def employees_data():
    """Фикстура данных для создания сотрудника."""
    data = {
        'full_name': 'Тестовый сотрудник',
        'position': 'Тестовая должность'
    }
    return data


@pytest.fixture
def employees_bad_data():
    """Фикстура создания сотрудника."""
    data = {
        'full_name': '',
        'position': 'Тестовая должность'
    }
    return data
