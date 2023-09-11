from datetime import date

from ninja import Schema, ModelSchema

from todolist.apps.todos.models import Todo


class TodoSchema(ModelSchema):
    class Config:
        model = Todo
        model_fields = (
            'list',
            'title',
            'notes',
            'due_date',
        )


class TodoIn(Schema):
    list: int
    title: str
    status: str = None
    notes: str = None
    due_date: date = None


class TodoOut(Schema):
    id: int
    title: str
    status: str
    notes: str
    due_date: date = None
