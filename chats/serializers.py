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
    class Meta:
        model = User
        fields = ['image', 'username', 'tg_id', 'first_name', 'last_name']