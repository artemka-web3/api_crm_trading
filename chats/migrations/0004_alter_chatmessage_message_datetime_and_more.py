# Generated by Django 5.0.1 on 2024-01-30 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='message_datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='message_sender',
            field=models.CharField(max_length=255),
        ),
    ]
