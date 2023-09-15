from django.contrib import admin

from todolist.apps.base.models import Address
from todolist.apps.todos.models import TodoList, Todo


class AddressInline(admin.TabularInline):
    model = Address
    verbose_name_plural = 'Location Address'


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'todo_items_count')
    search_fields = ('title', 'owner__first_name', 'owner__last_name')
    list_filter = ('owner',)
    ordering = ('-created_at',)

    # Add a summary field to the change form
    readonly_fields = ('summary',)

    @staticmethod
    def todo_items_count(obj):
        return obj.todo_items_count


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'list', 'due_date', 'created_at')
    search_fields = ('title', 'list__title')
    list_filter = ('status', 'list', 'due_date')
    ordering = ('due_date', '-created_at')
    readonly_fields = ('location',)
