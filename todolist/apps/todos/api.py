from typing import List

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

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


@api_controller(auth=JWTAuth())
class TodosController(ControllerBase):
    @staticmethod
    def get_qs(user: User) -> QuerySet[Todo]:
        return Todo.objects.get(list__owner=user)

    @staticmethod
    def get_list_qs(user: User) -> QuerySet[TodoList]:
        return TodoList.objects.filter(owner=user)

    @http_get('/todos', response=List[TodoOut], by_alias=True)
    @paginate(PageNumberPagination)
    def list_todos(self, request, list_id: int = 1) -> List[Todo]:
        todo_list = self.get_object_or_exception(self.get_qs(request.user), list__id=list_id)
        return todo_list.todo_items

    @http_post('/todos', response=TodoOut, by_alias=True)
    def create_todo(self, request, data: TodoIn) -> Todo:
        todo_list, created = self.get_qs(request.user).get_or_create(id=getattr(data, 'list'), owner=request.user)
        return Todo.objects.create(data.dict(), list=todo_list)

    @http_get('/todos/{todo_id}', response=TodoOut, by_alias=True)
    def get_todo(self, request, todo_id: int) -> Todo:
        return get_object_or_404(self.get_qs(request.user), id=todo_id)

    @http_post('/todos', response=TodoOut, by_alias=True)
    def create_todo(self, _request, payload: TodoIn) -> Todo:
        return Todo.objects.create(**payload.dict())

    @http_put('/todos/{todo_id}', response=TodoOut, by_alias=True)
    def update_todo(self, request, todo_id: int, payload: TodoIn) -> Todo:
        todo = get_object_or_404(self.get_qs(request.user), id=todo_id)
        for k, v in payload.dict().items():
            setattr(todo, k, v)
        todo.save()
        return todo

    @http_delete('/todos/{todo_id}', response=None)
    def delete_todo(self, request, todo_id: int) -> None:
        self.get_object_or_exception(self.get_qs(request.user), id=todo_id).delete()

    @http_get('/todos/lists', response=TodoListSchema, by_alias=True)
    @paginate(PageNumberPagination)
    def list_todo_lists(self, request):
        return self.get_qs(request.user)

    @http_get('/todos/lists/{id}', response=TodoListSchema, by_alias=True)
    def get_todo_list(self, request, list_id: int):
        return self.get_object_or_exception(self.get_qs(request.user), id=list_id)

    @http_post('/todos/lists', response=TodoListSchema, by_alias=True)
    def create_todo_list(self, request, title: str) -> TodoList:
        return TodoList.objects.create(owner=request.user, title=title)

    @http_patch('/todos/lists/{id}', response=TodoListSchema, by_alias=True)
    def partial_update_todo_list(self, request, list_id: int, payload: TodoListSchema) -> TodoList:
        todolist = self.get_object_or_exception(self.get_qs(request.user), id=list_id)
        for k, v in payload.dict().items():
            setattr(todolist, k, v)

        todolist.save()
        return todolist

    @http_delete('/todos/lists/{id}', response=None, by_alias=True)
    def delete_todo_list(self, request, list_id: int) -> None:
        self.get_object_or_exception(self.get_qs(request.user), id=list_id).delete()
