# Generated by Django 4.1.3 on 2022-11-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_chatroom_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='user',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='room_name',
            field=models.CharField(default='all-room', max_length=10),
        ),
    ]
