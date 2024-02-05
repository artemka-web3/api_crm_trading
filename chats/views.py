# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ChatMessage, User
from .serializers import ChatMessageSerializer, ChatsSerializer, UserSerializer
import requests

class ChatMessageList(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

class ChatMessageListByChatId(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        # Get the chat_id from the request parameters (assuming it's in the query parameters)
        chat_id = self.request.query_params.get('chat_id', None)

        # Filter and order the queryset based on the provided chat_id
        if chat_id:
            try:
                # Retrieve the User object based on tg_id
                user = User.objects.get(tg_id=chat_id)
                
                # Filter and order the queryset based on the provided chat_id
                return ChatMessage.objects.filter(user=user).order_by('message_datetime')
            except User.DoesNotExist:
                # Handle the case where the user with the provided chat_id doesn't exist
                return ChatMessage.objects.none()
        else:
            return ChatMessage.objects.all().order_by('message_datetime')

class ChatsList(generics.ListCreateAPIView):
    serializer_class = ChatsSerializer
    queryset = ChatMessage.objects.all()


class ChatMessageCreate(generics.CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SendTelegramMessageView(generics.CreateAPIView):
    """
    A view to trigger the sending of a Telegram message.
    """
    def post(self, request, *args, **kwargs):
        # Get the chat_id and message from the request data
        chat_id = request.data.get('chat_id')
        message = request.data.get('message')

        if not chat_id or not message:
            return Response({"error": "chat_id and message are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Call the function to send a message via Telegram bot
        send_telegram_message(chat_id, message)

        return Response({"message": "Telegram message sent successfully"}, status=status.HTTP_200_OK)

# ... (other views)

def send_telegram_message(chat_id, message):
    bot_token = '6528585494:AAGKnFWegrkgJyiR3OV5GmvYFRMtQ5hTte4'
    telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    params = {
        'chat_id': chat_id,
        'text': message,
    }

    try:
        response = requests.post(telegram_api_url, params=params)
        response.raise_for_status()
        # Optionally, you can handle the response here
    except requests.RequestException as e:
        # Handle errors (e.g., log them)
        print(f"Error sending Telegram message: {e}")