from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from todolist.apps.people.views import TodoViewSet, TodoListViewSet

drf_router = DefaultRouter()
drf_router.register(r'todos', TodoViewSet, basename='todos'),
drf_router.register(r'todos/lists', TodoListViewSet, basename='todo-lists'),
