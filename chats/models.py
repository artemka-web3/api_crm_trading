from django.db import models

class User(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    tg_id = models.IntegerField(unique=True, primary_key = True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.IntegerField()
    message_text = models.TextField(default="", blank=False)
    message_datetime = models.DateTimeField()
    message_sender = models.CharField(max_length=255)