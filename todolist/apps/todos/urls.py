from rest_framework.routers import DefaultRouter

from todolist.apps.todos.views import TodoViewSet, TodoListViewSet

drf_router = DefaultRouter()
drf_router.register(r'todos', TodoViewSet, basename='todos'),
drf_router.register(r'todos/lists', TodoListViewSet, basename='todo-lists'),
