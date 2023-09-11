from ninja import ModelSchema
from ninja.orm import create_schema

from todolist.apps.todos.models import Todo, TodoList


def to_camel(string: str) -> str:
    camel_string = ''

    for i, word in enumerate(string.split('_')):
        if i == 0:
            camel_string += word
        else:
            camel_string += word.capitalize()

    return camel_string


class TodoSchemaBase(ModelSchema):
    class Config:
        model = Todo
        model_fields = ['title', 'status', 'notes', 'due_date']


class TodoIn(TodoSchemaBase, ModelSchema):
    class Config(TodoSchemaBase.Config):
        model_fields = [*TodoSchemaBase.Config.model_fields, 'list']


class TodoOut(TodoSchemaBase, ModelSchema):
    class Config(TodoSchemaBase.Config):
        model_fields = [*TodoSchemaBase.Config.model_fields, 'id']
        alias_generator = to_camel


class TodoListSchema(ModelSchema):
    class Config:
        model = TodoList
        model_fields = ['title']
        alias_generator = to_camel
