# Generated by Django 4.2.5 on 2023-09-13 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'todo_lists',
                'db_table': 'todo_lists',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('DUE', 'Due'), ('COMPLETED', 'Completed'), ('DISMISSED', 'Dismissed')], default='PENDING')),
                ('notes', models.CharField(max_length=512, null=True)),
                ('due_date', models.DateField(null=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_items', to='todos.todolist')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.address')),
            ],
            options={
                'verbose_name_plural': 'todos',
                'db_table': 'todos',
                'ordering': ('due_date', '-created_at'),
            },
        ),
    ]
