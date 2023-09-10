# Generated by Django 4.2.5 on 2023-09-10 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_alter_person_options_alter_todo_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lists', to='todos.person'),
        ),
    ]