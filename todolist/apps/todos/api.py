from typing import List

from django.contrib.auth.models import User
from django.db.models import QuerySet

from ninja.pagination import PageNumberPagination
from ninja_extra import (
    ControllerBase,
    api_controller,
    http_delete,
    http_get,
    http_patch,
    http_post,
    http_put,
    paginate,
)
from ninja_jwt.authentication import JWTAuth

from todolist.apps.todos.models import Todo, TodoList
from todolist.apps.todos.schemas import TodoIn, TodoOut, TodoListSchema
from todolist.utils import update_from_payload


@api_controller(auth=JWTAuth())
class TodosController(ControllerBase):
    @staticmethod
    def get_qs(user: User) -> QuerySet[Todo]:
        return Todo.objects.get(list__owner=user)

    @staticmethod
    def get_list_qs(user: User) -> QuerySet[TodoList]:
        return TodoList.objects.filter(owner=user)

    @staticmethod
    def get_todo_list_with_todos(list_id: int) -> TodoList:
        return TodoList.objects.get(id=list_id).prefetch_related('todo_items')

    @http_get('/todos', response=List[TodoOut], by_alias=True)
    @paginate(PageNumberPagination)
    def list_todos(self, request, list_id: int) -> List[Todo]:
        todo_list = self.get_object_or_exception(self.get_qs(request.user), list__id=list_id)
        return todo_list.todo_items

    @http_get('/todos/{todo_id}', response=TodoOut, by_alias=True)
    def get_todo(self, request, todo_id: int) -> Todo:
        return self.get_object_or_exception(self.get_qs(request.user), id=todo_id)

    @http_get('/todos/lists', response=TodoListSchema, by_alias=True)
    @paginate(PageNumberPagination)
    def list_todo_lists(self, request) -> QuerySet[TodoList]:
        return self.get_list_qs(request.user)

    @http_get('/todos/lists/{list_id}', response=TodoListSchema, by_alias=True)
    def get_todo_list(self, request, list_id: int) -> TodoList:
        return self.get_todo_list_with_todos(list_id)

    @http_post('/todos', response=TodoOut, by_alias=True)
    def create_todo(self, _request, payload: TodoIn) -> Todo:
        return Todo.objects.create(**payload.dict())

    @http_post('/todos/lists', response=TodoListSchema, by_alias=True)
    def create_todo_list(self, request, title: str) -> TodoList:
        return TodoList.objects.create(owner=request.user, title=title)

    @http_patch('/todos/{todo_id}', response=TodoOut, by_alias=True)
    def partial_update_todo(self, request, todo_id: int, payload: TodoIn) -> Todo:
        todo = self.get_object_or_exception(self.get_qs(request.user), id=todo_id)
        return update_from_payload(todo, payload)

    @http_patch('/todos/lists/{list_id}', response=TodoListSchema, by_alias=True)
    def partial_update_todo_list(self, request, list_id: int, payload: TodoListSchema) -> TodoList:
        todolist = self.get_object_or_exception(self.get_qs(request.user), id=list_id)
        return update_from_payload(todolist, payload)

    @http_delete('/todos/{todo_id}', response=None)
    def delete_todo(self, request, todo_id: int) -> None:
        self.get_object_or_exception(self.get_qs(request.user), id=todo_id).delete()

    @http_delete('/todos/lists/{list_id}', response=None, by_alias=True)
    def delete_todo_list(self, request, list_id: int) -> None:
        self.get_object_or_exception(self.get_qs(request.user), id=list_id).delete()
