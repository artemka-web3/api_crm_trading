# Generated by Django 5.0.1 on 2024-02-06 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0005_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
