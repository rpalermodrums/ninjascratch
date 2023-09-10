from typing import List

from ninja import Router

from todolist.apps.todos.models import Todo, TodoList
from todolist.apps.todos.schemas import TodoIn, TodoOut

router = Router()


@router.post('/todos', response=TodoOut)
def create_todo(request, data: TodoIn) -> Todo:
    todo_list, created = TodoList.objects.get_or_create(id=data.list, owner_id=request.user.id)
    todo = Todo.objects.create(**{**data.dict(), 'list': todo_list})
    return todo


@router.get('/todos', response=List[TodoOut])
def list_todos(request, list_id: int = 1) -> List[Todo]:
    if request.user.id is not None:
        todo_list_qs = TodoList.objects.filter(owner=request.user.id)
    else:
        todo_list_qs = TodoList.objects.all()
    todo_list, created = todo_list_qs.get_or_create(pk=list_id)
    return todo_list.todo_items
