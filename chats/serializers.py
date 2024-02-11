# serializers.py
from rest_framework import serializers
from .models import ChatMessage, User

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['tg_id']
        
    def get_tg_id(self, obj):
        # Access the related User's tg_id
        return obj.user.tg_id
        
class UserSerializer(serializers.ModelSerializer):
    latest_unread_message_date = serializers.SerializerMethodField()
    unread_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['image', 'username', 'tg_id', 'first_name', 'last_name', 'captcha', 'latest_unread_message_date', 'unread_messages_count']

    def get_latest_unread_message_date(self, obj):
        return obj.get_latest_unread_message_date()

    def get_unread_messages_count(self, obj):
        return obj.get_unread_messages_count()