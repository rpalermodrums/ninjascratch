# Standard library imports
from typing import List

# Third-party imports
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import PageNumberPagination, paginate
from ninja_jwt.authentication import JWTAuth

# Local application imports
from todolist.apps.todos.models import Todo, TodoList
from todolist.apps.todos.schemas import TodoIn, TodoOut, TodoListSchemaBase
from todolist.utils import update_from_kv

router = Router()

endpoint_config = {
    'auth': JWTAuth(),
    'by_alias': True
}


@router.get('/todos', response=List[TodoOut], **endpoint_config)
@paginate(PageNumberPagination)
def list_todos(request, list_id: int) -> List[TodoOut]:
    todo_list = get_object_or_404(Todo.get_todo_qs(user=request.user), list__id=list_id)
    return todo_list.todo_items


@router.post('/todos', response=TodoOut, **endpoint_config)
def create_todo(request, payload: TodoIn) -> Todo:
    todo_list = get_object_or_404(TodoList.get_list_qs(user=request.user), id=payload.dict()['list'].id)
    return Todo.objects.create(**payload.dict(), list=todo_list)


@router.get('/todos/{int:todo_id}', response=TodoOut, **endpoint_config)
def get_todo(request, todo_id: int) -> Todo:
    return get_object_or_404(Todo.get_todo_qs(request.user), id=todo_id)


@router.patch('/todos/{int:todo_id}', response=TodoOut, **endpoint_config)
def partial_update_todo(request, todo_id: int, payload: TodoIn) -> Todo:
    todo_instance = get_object_or_404(Todo.get_todo_qs(user=request.user), id=todo_id)
    return update_from_kv(instance=todo_instance, kv=payload.dict())


@router.delete('/todos/{int:todo_id}', response=None, **endpoint_config)
def delete_todo(request, todo_id: int) -> None:
    get_object_or_404(Todo.get_todo_qs(user=request.user), id=todo_id).delete()


@router.get('/todos/lists', response=List[TodoListSchemaBase], **endpoint_config)
@paginate(PageNumberPagination)
def list_todo_lists(request) -> QuerySet[TodoList]:
    return TodoList.get_list_qs(user=request.user)


@router.post('/todos/lists', response=TodoListSchemaBase, **endpoint_config)
def create_todo_list(request, payload: TodoListSchemaBase) -> TodoList:
    return TodoList.objects.create(owner=request.user, **payload.dict())


@router.get('/todos/lists/{int:list_id}', response=TodoListSchemaBase, **endpoint_config)
def get_todo_list(_request, list_id: int) -> TodoList:
    return TodoList.get_todo_list_with_todos_qs(list_id=list_id)


@router.patch('/todos/lists/{int:list_id}', response=TodoListSchemaBase, **endpoint_config)
def partial_update_todo_list(request, list_id: int, payload: TodoListSchemaBase) -> TodoList:
    todolist_instance = get_object_or_404(TodoList.get_list_qs(user=request.user), id=list_id)
    return update_from_kv(instance=todolist_instance, kv=payload.dict())


@router.delete('/todos/lists/{int:list_id}', response=None, **endpoint_config)
def delete_todo_list(request, list_id: int) -> None:
    get_object_or_404(TodoList.get_list_qs(user=request.user), id=list_id).delete()
