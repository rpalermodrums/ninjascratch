from rest_framework.routers import DefaultRouter

from todolist.apps.todos.views import TodoViewSet, TodoListViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos'),
router.register(r'todos/lists', TodoListViewSet, basename='todo-lists'),
