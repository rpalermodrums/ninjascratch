from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from ninja.pagination import PageNumberPagination, paginate
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from todolist.apps.todos.models import Todo, TodoList
from todolist.apps.todos.schemas import TodoIn, TodoOut, TodoListSchemaBase
from todolist.utils import update_from_kv

router = Router()


todo_config = {'response': TodoOut, 'auth': JWTAuth(), 'by_alias': True}


@router.get('/todos', **{**todo_config, 'response': list[TodoOut]})
@paginate(PageNumberPagination)
def list_todos(request, list_id: int) -> list[TodoOut]:
    todo_list = get_object_or_404(Todo.get_todo_qs(request.user), list__id=list_id)
    return todo_list.todo_items


@router.get('/todos/{todo_id}', **todo_config)
def get_todo(request, todo_id: int) -> Todo:
    return get_object_or_404(Todo.get_todo_qs(request.user), id=todo_id)


@router.post('/todos', **todo_config)
def create_todo(_request, payload: TodoIn) -> Todo:
    return Todo.objects.create(**payload.dict())


@router.patch('/todos/{todo_id}', **todo_config)
def partial_update_todo(request, todo_id: int, payload: TodoIn) -> Todo:
    todo = get_object_or_404(Todo.get_todo_qs(request.user), id=todo_id)
    return update_from_kv(todo, payload.dict())


@router.delete('/todos/{todo_id}', **{**todo_config, 'response': None})
def delete_todo(request, todo_id: int) -> None:
    get_object_or_404(Todo.get_todo_qs(request.user), id=todo_id).delete()


todo_list_config = {'response': TodoListSchemaBase, 'auth': JWTAuth(), 'by_alias': True}


@router.get('/todos/lists', **{**todo_list_config, 'response': list[TodoListSchemaBase]})
@paginate(PageNumberPagination)
def list_todo_lists(request) -> QuerySet[TodoList]:
    return TodoList.get_list_qs(request.user)


@router.get('/todos/lists/{list_id}', **todo_list_config)
def get_todo_list(_request, list_id: int) -> TodoList:
    return TodoList.get_todo_list_with_todos_qs(list_id)


@router.post('/todos/lists', **todo_list_config)
def create_todo_list(request, title: str) -> TodoList:
    return TodoList.objects.create(owner=request.user, title=title)


@router.patch('/todos/lists/{list_id}', **todo_list_config)
def partial_update_todo_list(request, list_id: int, payload: TodoListSchemaBase) -> TodoList:
    todolist = get_object_or_404(TodoList.get_list_qs(request.user), id=list_id)
    return update_from_kv(todolist, payload.dict())


@router.delete('/todos/lists/{list_id}', **{**todo_list_config, 'response': None})
def delete_todo_list(request, list_id: int) -> None:
    get_object_or_404(TodoList.get_list_qs(request.user), id=list_id).delete()
