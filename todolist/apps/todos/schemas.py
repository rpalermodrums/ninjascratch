from ninja import ModelSchema

from todolist.apps.todos.models import Todo


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
