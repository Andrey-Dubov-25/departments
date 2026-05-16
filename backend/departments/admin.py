from django.contrib import admin

from .models import Department, Employee


admin.site.empty_value_display = 'Не задано'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Модель подразделений в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиска;
    - ordering: поля для сортировки списка.

    Значения полей:
    * name - название подразделения;
    * parent - родительское подразделение;
    * craeted_at - время создания подразделения.
    """

    list_display = ('name', 'parent', 'created_at')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Модель сотрудников в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиск;
    - ordering: поля для сортировки списка.

    Значения полей:
    * full_name - имя сотрудника;
    * position - должность сотрудника;
    * department - подразделение сотрудника;
    * hired_at - дата устройства сотрудника;
    * craeted_at - время создания записи о сотруднике.

    """

    list_display = (
        'full_name', 'position', 'department', 'hired_at', 'created_at'
    )
    search_fields = ('full_name',)
    list_filter = ('full_name',)
    ordering = ('full_name',)
