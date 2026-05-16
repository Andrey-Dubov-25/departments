from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from departments.models import Department, Employee
from .serializers import (
    DepartmentSerializer,
    DepartmentUpdateSerializer,
    EmployeesCreateSerializer,
    DepartmentDeleteSerializer
)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с подразделениями, в котором реализованы CRUD-операции
    (без PUT) и добавление сотрудников.
    """

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        """Возвращает информацию о подразделении."""
        return Department.objects.select_related('parent').prefetch_related(
            'employees',
            'children'
        )

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от действия."""

        if self.action in ['partial_update', 'create']:
            return DepartmentUpdateSerializer

        elif self.action == 'employees':
            return EmployeesCreateSerializer

        elif self.action == 'destroy':
            return DepartmentDeleteSerializer

        return DepartmentSerializer

    @action(detail=True, methods=['POST'])
    def employees(self, request, pk=None):
        """Создание сотрудника в подразделении."""
        department = get_object_or_404(Department, pk=pk)
        serializer = EmployeesCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save(department=department)
        return Response(
            EmployeesCreateSerializer(employee).data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает информацию о подразделении в зависимости от параметров:
        - depth (int, опционально): глубина вложенности дочерних подразделений
        (1–5, по умолчанию 1);
        - include_employees (bool, опционально): включать ли список сотрудников
        (по умолчанию true).
        """
        department_id = kwargs['pk']

        depth = int(request.query_params.get('depth', 1))
        depth = max(1, min(depth, 5))

        include_employees = request.query_params.get(
            'include_employees', 'true'
        ).lower() == 'true'

        department = get_object_or_404(Department, id=department_id)

        serializer = DepartmentSerializer(
            department,
            context={
                'depth': depth,
                'include_employees': include_employees
            }
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет подразделение в зависимости от параметра mode:

        - cascade: удаляет подразделение и всех его сотрудников;
        - reassign: переназначает сотрудников в другое подразделение
        (требуется указать reassign_to_department_id).

        Ограничения:
        - reassign_to_department_id не может быть ID удаляемого подразделения;
        - целевое подразделение для переназначения не должно находиться в
        поддереве удаляемого;
        - подразделение для переназначения должно существовать.
        """
        instance = self.get_object()
        mode = request.query_params.get('mode', 'cascade')
        reassign_to_department_id = request.query_params.get(
            'reassign_to_department_id'
        )

        data = {
            'mode': mode,
            'reassign_to_department_id': reassign_to_department_id
        }

        serializer = DepartmentDeleteSerializer(
            data=data, context={'department_id': instance.id}
        )

        serializer.is_valid(raise_exception=True)
        mode = serializer.validated_data.get('mode')

        if mode == 'reassign':
            reassign_department = serializer.validated_data.get(
                'reassign_department'
            )
            Employee.objects.filter(department=instance).update(
                department=reassign_department
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
