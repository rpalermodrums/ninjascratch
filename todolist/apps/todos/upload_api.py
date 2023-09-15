import csv
import random
from io import StringIO

from ninja import UploadedFile, File, Router
from ninja_jwt.authentication import JWTAuth

from todolist.apps.todos.models import TodoList, Todo
from todolist.apps.todos.schemas import TodoOut
from todolist.utils import update_from_kv

router = Router()


upload_config = {'auth': JWTAuth(), 'response': list[TodoOut], 'by_alias': True}


@router.post('/todos/bulk-create', **upload_config)
def upload_todos(_request, file: UploadedFile = File(...)):
    rows = []

    for row in csv.DictReader(StringIO(file.read().decode())):
        # noinspection PyTypeChecker
        todo_list, created = TodoList.objects.get_or_create(id=row['list'])
        if created:
            todo_list.name = f'Todo List {random.randint(16, 32)}'
            todo_list.save()
        rows.append(Todo.objects.create(**{**row, 'list': todo_list}))

    return rows


@router.patch('/todos/bulk-update', **upload_config)
def bulk_update_todos(_request, file: UploadedFile = File(...)):
    rows = []

    for row in csv.DictReader(StringIO(file.read().decode())):
        # noinspection PyTypeChecker
        update_from_kv(Todo.objects.get(id=row['id']), row)
        # noinspection PyArgumentList
        rows.append(**row)

    return rows


@router.post('/todos/validate', **{**upload_config, 'response': None})
def validate_todos_csv(_request, _file: UploadedFile = File(...)):
    pass
