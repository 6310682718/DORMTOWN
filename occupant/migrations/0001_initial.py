# Generated by Django 4.1.2 on 2022-11-05 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=3)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_level', models.CharField(max_length=5)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StatusType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=20)),
                ('zip_code', models.CharField(max_length=10)),
                ('role_id', models.ForeignKey(default='5', on_delete=django.db.models.deletion.CASCADE, related_name='role_id', to='occupant.role')),
                ('room_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='room_id', to='occupant.room')),
                ('user_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='room_type', to='occupant.roomtype'),
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('create_at', models.DateTimeField()),
                ('room_type', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='reserved_room_type', to='occupant.roomtype')),
                ('status_type', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='status_type', to='occupant.statustype')),
                ('user_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='reserved_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('note', models.CharField(max_length=150)),
                ('assign_to_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='assign_to_id', to=settings.AUTH_USER_MODEL)),
                ('from_user_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='from_user_id', to=settings.AUTH_USER_MODEL)),
                ('problem_type_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='problem_type_id', to='occupant.problemtype')),
                ('role_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='reported_role_id', to='occupant.role')),
                ('status_id', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='status_id', to='occupant.statustype')),
            ],
        ),
    ]
