# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ChatMessage, User
from .serializers import ChatMessageSerializer, ChatsSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models.functions import Coalesce
from django.db.models  import Count
from django.db.models import IntegerField
from django.db.models import Max 
from django.db import models
import requests


class GetCaptchaValue(APIView):
    def get(self, request, *args, **kwargs):
        # Получите tg_id из параметра запроса
        tg_id = request.query_params.get('tg_id')

        if not tg_id:
            return Response({"error": "tg_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Получите объект пользователя на основе tg_id
            user = User.objects.get(tg_id=tg_id)

            # Сериализуйте и верните значение поля captcha
            data = {"tg_id": tg_id, "captcha": user.captcha}
            return Response(data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # Обработайте случай, когда пользователя с указанным tg_id не существует
            return Response({"error": f"User with tg_id {tg_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Обработайте другие исключения при необходимости
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetCaptchaTrue(APIView):
    def post(self, request, *args, **kwargs):
        # Получите tg_id из данных запроса
        tg_id = request.data.get('tg_id')

        if not tg_id:
            return Response({"error": "tg_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Получите объект пользователя на основе tg_id
            user = User.objects.get(tg_id=tg_id)
            
            # Измените значение поля captcha на True
            user.captcha = True
            user.save()

            # Сериализуйте и верните обновленного пользователя
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # Обработайте случай, когда пользователя с указанным tg_id не существует
            return Response({"error": f"User with tg_id {tg_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Обработайте другие исключения при необходимости
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ResetUnreadMessages(APIView):
    def post(self, request, *args, **kwargs):
        # Get tg_id from the request data
        tg_id = request.query_params.get('tg_id', None)

        if not tg_id:
            return Response({"error": "tg_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the user object based on tg_id
            user = User.objects.get(tg_id=tg_id)

            # Set unread_messages to zero
            user.chatmessage_set.filter(read=False).update(read=True)

            # Serialize and return the updated user
            # You may customize the serializer based on your needs
            # For simplicity, assuming you have a UserSerializer
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": f"User with tg_id {tg_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.annotate(
            unread_messages_count=Coalesce(Count('chatmessage', filter=models.Q(chatmessage__read=False)), 0, output_field=IntegerField()),
            latest_unread_message_date=Max('chatmessage__message_datetime', filter=models.Q(chatmessage__read=False))
        ).order_by('-latest_unread_message_date')

        return queryset
    

class UnreadMessagesCountView(APIView):
    def get(self, request, tg_id):
        try:
            user = User.objects.get(tg_id=tg_id)
            unread_messages_count = user.get_unread_messages_count()
            return Response({'unread_messages_count': unread_messages_count}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


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
    bot_token = '6523327515:AAHGjbhRrv3HiUq-d0cGbp3MAmrMvFJriNM'
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