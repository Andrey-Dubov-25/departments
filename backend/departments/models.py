from django.db import models

from . import constants


class Department(models.Model):
    """Модель подразделения."""
    name = models.CharField(
        max_length=constants.NAME_LEN,
        verbose_name='Название',
        help_text='Название подразделения'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Подразделение',
        help_text='Подразделение',
        related_name='children'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'подразделение'
        verbose_name_plural = 'Подразделения'
        unique_together = ('name', 'parent_id')

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Модель сотрудника."""
    full_name = models.CharField(
        max_length=constants.FULL_NAME_LEN,
        verbose_name='Имя',
        help_text='Имя сотрудника'
    )
    position = models.CharField(
        max_length=constants.POSITION_LEN,
        verbose_name='Должность',
        help_text='Должность сотрудника'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name='Подразделение',
        help_text='Подразделение',
        related_name='employees'
    )
    hired_at = models.DateField(
        null=True,
        blank=True,
        verbose_name='Нанят',
        help_text='Нанят'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name
