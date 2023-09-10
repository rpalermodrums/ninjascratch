from typing import List

from ninja import Router

from todolist.apps.todos.models import Todo, TodoList
from todolist.apps.todos.schemas import TodoIn, TodoOut

router = Router()


@router.post('/todos', response=TodoOut)
def create_todo(request, data: TodoIn):
    print('create_todo')
    todo_list = TodoList.objects.get_or_create(id=data.list, owner_id=request.user.id)
    print('todo_list')
    todo = Todo.objects.create(**data.dict(), list=todo_list)
    return todo


@router.get('/todos', response=List[TodoOut])
def list_todos(request, list_id: int = 1):
    todo_list = TodoList.objects.filter(owner=request.user).get(pk=list_id)
    return todo_list.todo_items
