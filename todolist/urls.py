"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

from todolist.apps.todos.upload_api import router as csv_router
from todolist.apps.todos.urls import router as drf_router
from todolist.apps.todos.api import router as todos_router

api = NinjaExtraAPI(urls_namespace='ninja')
csv_upload_api = NinjaExtraAPI(urls_namespace='upload')
api.register_controllers(
    NinjaJWTDefaultController,
)

api.add_router('/upload', csv_router)
api.add_router('/todos', todos_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api/', api.urls),
    path('drf/', include(drf_router.urls))
]
