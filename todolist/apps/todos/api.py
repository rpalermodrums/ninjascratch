import logging
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from todolist.apps.todos.models import Todo, TodoList
from todolist.apps.todos.schemas import TodoIn, TodoOut

router = Router(auth=JWTAuth())


@router.post('/todos', response=TodoOut)
def create_todo(request, data: TodoIn) -> Todo:
    todo_list, created = TodoList.objects.get_or_create(id=data.list, owner_id=request.user.id)
    todo = Todo.objects.create(**{**data.dict(), 'list': todo_list})
    return todo


@router.get('/todos', response=List[TodoOut])
def list_todos(request, list_id: int = 1) -> List[Todo]:
    todo_list = get_object_or_404(TodoList, id=list_id)
    return todo_list.todo_items


@router.get('/todos/{todo_id}', response=TodoOut)
def get_todo(request, todo_id: int):
    return get_object_or_404(Todo, id=todo_id)


@router.post('/todos', response=TodoOut)
def create_todo(request, payload):
    todo = Todo.objects.create(**payload.dict())
    return todo


@router.put('/todos/{todo_id}', response=TodoOut)
def update_todo(request, todo_id: int, payload):
    todo = get_object_or_404(Todo, id=todo_id)
    for attr, value in payload.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo