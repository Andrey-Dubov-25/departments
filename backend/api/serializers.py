from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from departments import constants
from departments.models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор получения информации о сотруднике."""
    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'position', 'hired_at', 'created_at')


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор получения информации о подразделении."""
    employees = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('id', 'name', 'employees', 'children', 'created_at')

    def get_employees(self, obj):
        """Получение сотрудников подразделения."""
        include_employees = self.context.get('include_employees', True)

        if not include_employees:
            return []

        employees = obj.employees.all().order_by('created_at', 'full_name')
        serializer = EmployeeSerializer(employees, many=True)
        return serializer.data

    def get_children(self, obj):
        """Получение дочерних подразделений."""
        depth = self.context.get('depth', 1)
        include_employees = self.context.get('include_employees', True)

        if depth <= 0:
            return []

        children = obj.children.select_related('parent').prefetch_related(
            'employees' if include_employees else None
        )
        serializer = DepartmentSerializer(
            children,
            many=True,
            context={
                'depth': depth - 1,
                'include_employees': include_employees
            }
        )
        return serializer.data


class DepartmentUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения родительского подразделения."""
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Department
        fields = ('name', 'parent')

    def validate_name(self, value):
        """Валидация поля name при создании."""

        if not value or not value.strip():
            raise ValidationError('Название не может быть пустым')

        return value.strip()

    def validate_parent(self, value):
        """Валидация поля parent."""

        if value is not None and not Department.objects.filter(
            id=value.id
        ).exists():
            raise serializers.ValidationError(
                'Родительское подразделение не существует'
            )

        return value

    def validate(self, data):
        """Валидация передачи полей name и parent."""
        name = data.get('name')
        parent = data.get('parent')

        department_exist = Department.objects.filter(name=name, parent=parent)

        if self.instance:
            department_exist = department_exist.exclude(pk=self.instance.pk)

        if department_exist.exists():

            if parent:
                raise ValidationError(
                    f'Подразделение с названием "{name}" уже существует в '
                    f'подразделении {parent}.'
                )

            else:
                raise ValidationError(
                    f'Подразделение с названием "{name}" уже существует на '
                    'верхнем уровне.'
                )

        if parent and self.is_cycle(parent, self.instance):
            raise ValidationError('В организационной структуре получен цикл')

        return data

    @staticmethod
    def is_cycle(new_parent, current_instance):
        """Проверка на создание цикла при изменении родителя."""

        if new_parent is None:
            return False

        current = new_parent
        visited = set()

        while current:

            if current.id in visited:
                return True

            visited.add(current.id)

            if current == current_instance:
                return True

            current = current.parent

        return False


class EmployeesCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания сотрудника."""
    full_name = serializers.CharField(max_length=constants.FULL_NAME_LEN)
    position = serializers.CharField(max_length=constants.POSITION_LEN)
    hired_at = serializers.DateField(required=False, allow_null=True)

    def validate_full_name(self, value):
        """Валидация поля full_name."""

        if not value or not value.strip():
            raise ValidationError('Нельзя оставлять поле full_name пустым.')

        return value.strip()

    def validate_position(self, value):
        """Валидация поля position."""

        if not value or not value.strip():
            raise ValidationError('Нельзя оставлять поле position пустым.')

        return value.strip()

    class Meta:
        model = Employee
        fields = ('full_name', 'position', 'hired_at')


class DepartmentDeleteSerializer(serializers.Serializer):
    """Сериалитор удаления подразделения."""
    mode = serializers.ChoiceField(
        choices=['cascade', 'reassign'],
        default='cascade'
    )
    reassign_to_department_id = serializers.IntegerField(
        required=False, allow_null=True
    )

    def validate(self, data):
        """Валидация передачи параметров mode и reassign_to_department_id."""
        mode = data.get('mode')
        reassign_to_department_id = data.get('reassign_to_department_id')
        current_department_id = self.context.get('department_id')

        if mode == 'reassign':

            if reassign_to_department_id is None:
                raise ValidationError(
                    {'reassign_to_department_id': 'Обязательный параметр'}
                )

            reassign_department = get_object_or_404(
                Department, id=reassign_to_department_id
            )

            if (
                reassign_to_department_id
                and reassign_department.id == current_department_id
            ):
                raise ValidationError(
                    'Нельзя переназначить сотрудников в подразделение, '
                    'которое удаляется'
                )

            if self.is_in_tree(reassign_department, current_department_id):
                raise ValidationError(
                    'Подразделение для перемещения тоже удалится'
                )

            data['reassign_department'] = reassign_department
        return data

    @staticmethod
    def is_in_tree(target_department, parent_id):
        """
        Проверяет, находится ли target_department в поддереве подразделения с
        parent_id. Возвращает True, если target_department — потомок parent_id.
        """
        current = target_department.parent

        while current:

            if current.id == parent_id:
                return True

            current = current.parent

        return False
