# Generated by Django 5.0.1 on 2024-02-06 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0008_alter_user_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tg_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
