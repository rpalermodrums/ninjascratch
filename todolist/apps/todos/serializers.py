from rest_framework import serializers
from todolist.apps.todos import models


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Todo
        fields = (
            'id',
            'title',
            'status',
            'notes',
            'due_date',
        )


class TodoListSerializer(serializers.ModelSerializer):
    todo_items = TodoSerializer(source='todo_items')
    class Meta:
        model = models.TodoList
        fields = (
            'id',
            'owner',
            'title',
            'todo_items',
        )
