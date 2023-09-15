from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from todolist.apps.base.models import AbstractTimestampedModel, Address


class TodoList(AbstractTimestampedModel, models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='lists', null=True)

    @cached_property
    def summary(self) -> dict[str, int]:
        status_map = {}
        for todo in self.todo_items.all():
            if str(todo.status) in status_map:
                status_map[str(todo.status)] += 1
            else:
                status_map[str(todo.status)] = 0

        return status_map

    @cached_property
    def todo_items_count(self) -> int:
        return self.todo_items.count()

    @classmethod
    def get_list_qs(cls, user: User) -> QuerySet[super.__class__]:
        return cls.objects.filter(owner=user)

    @classmethod
    def get_todo_list_with_todos_qs(cls, list_id: int) -> super.__class__:
        return cls.objects.prefetch_related('todo_items').get(id=list_id)

    class Meta:
        db_table = 'todo_lists'
        verbose_name_plural = 'todo_lists'
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.id} - {self.title} ({self.todo_items_count} todos)'


class Todo(AbstractTimestampedModel, models.Model):
    class TodoStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        DUE = 'DUE', _('Due')
        COMPLETED = 'COMPLETED', _('Completed')
        DISMISSED = 'DISMISSED', _('Dismissed')

    list = models.ForeignKey(to=TodoList, on_delete=models.CASCADE, related_name='todo_items')
    location = models.OneToOneField(to=Address, on_delete=models.DO_NOTHING, null=True)

    title = models.CharField(max_length=128)
    status = models.CharField(choices=TodoStatus.choices, default=TodoStatus.PENDING)
    notes = models.CharField(max_length=512, null=True)
    due_date = models.DateField(null=True)

    @classmethod
    def get_todo_qs(cls, user: User) -> QuerySet[super]:
        return cls.objects.select_related('list__owner').get(list__owner=user)

    class Meta:
        db_table = 'todos'
        verbose_name_plural = 'todos'
        ordering = ('due_date', '-created_at')

    def __str__(self):
        return f'{id} - {self.title} ({self.status})'
