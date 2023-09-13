# Generated by Django 4.2.5 on 2023-09-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=128)),
                ('address2', models.CharField(blank=True, max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name_plural': 'addresses',
                'db_table': 'addresses',
                'ordering': ('zip',),
            },
        ),
    ]
