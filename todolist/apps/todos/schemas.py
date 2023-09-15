from typing import List

from ninja import ModelSchema
from pydantic.utils import to_lower_camel

from todolist.apps.todos.models import Todo, TodoList


class TodoSchemaBase(ModelSchema):
    class Config:
        model = Todo
        model_fields = ['title', 'status', 'notes', 'due_date']
        alias_generator = to_lower_camel


class TodoIn(TodoSchemaBase, ModelSchema):
    class Config(TodoSchemaBase.Config):
        model_fields = [*TodoSchemaBase.Config.model_fields, 'list']


class TodoOut(TodoSchemaBase, ModelSchema):
    class Config(TodoSchemaBase.Config):
        model_fields = [*TodoSchemaBase.Config.model_fields, 'id']


class TodoListSchemaBase(ModelSchema):
    todo_items: List[TodoOut] = []

    class Config:
        model = TodoList
        model_fields = [
            'id',
            'owner',
            'title',
        ]
        alias_generator = to_lower_camel
