from ninja import ModelSchema

from todolist.apps.todos.models import Todo


def to_camel(string: str) -> str:
    camel_string = ''

    for i, word in enumerate(string.split('_')):
        if i == 0:
            camel_string += word
        else:
            camel_string += word.capitalize()

    print(camel_string)
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
