from rest_framework import viewsets

from todolist.apps.todos.models import Todo, TodoList
from todolist.apps.todos.serializers import TodoSerializer, TodoListSerializer


# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer

    def get_queryset(self) -> Todo:
        return Todo.objects.select_related('list__owner').filter(list__owner=self.request.user)


class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoListSerializer

    def get_queryset(self) -> TodoList:
        return TodoList.objects.filter(owner_id=self.request.user.id).prefetch_related('todo_items')