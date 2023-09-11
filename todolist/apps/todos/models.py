from django.contrib.auth.models import AbstractUser, Group, UserManager, Permission
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class AbstractTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractBaseModel(AbstractTimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class Address(models.Model):
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)

    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'addresses'
        ordering = ('zip', )


class Person(AbstractTimestampedModel, AbstractUser, models.Model):
    birthdate = models.DateField
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="person_set",
        related_query_name="person",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="person_set",
        related_query_name="person",
    )

    objects = UserManager()

    class Meta:
        db_table = 'people'
        verbose_name_plural = 'people'
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'


class TodoList(AbstractTimestampedModel, models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(to=Person, on_delete=models.CASCADE, related_name='lists', null=True)

    @cached_property
    def summary(self):
        status_map = {}
        for todo in self.todo_items.all():
            if str(todo.status) in status_map:
                status_map[str(todo.status)] += 1
            else:
                status_map[str(todo.status)] = 0

        return status_map

    @cached_property
    def todo_items_count(self):
        return self.todo_items.count()

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
    location = models.ForeignKey(to=Address, on_delete=models.DO_NOTHING, null=True)

    title = models.CharField(max_length=128)
    status = models.CharField(choices=TodoStatus.choices, default=TodoStatus.PENDING)
    notes = models.CharField(max_length=512, null=True)
    due_date = models.DateField(null=True)

    class Meta:
        db_table = 'todos'
        verbose_name_plural = 'todos'
        ordering = ('due_date', '-created_at')

    def __str__(self):
        return f'{id} - {self.title} ({self.status})'
