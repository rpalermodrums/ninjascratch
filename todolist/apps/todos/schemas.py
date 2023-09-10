from datetime import date

from ninja import Schema


class TodoIn(Schema):
    list: int
    title: str
    status: str = None
    notes: str = None
    due_date: date = None


class TodoOut(Schema):
    list: int
    id: int
    title: str
    status: str
    notes: str
    due_date: date
