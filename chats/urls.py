from django.urls import path
from .views import ChatMessageListByChatId, ChatMessageCreate, ChatsList, ChatMessageList, UserCreateView, UserListView, SendTelegramMessageView

urlpatterns = [
    path('api/messages/', ChatMessageListByChatId.as_view(), name='message-list'),
    path('api/all_messages/', ChatMessageList.as_view(), name='all-message-list'),
    path('api/users/', UserListView.as_view(), name='user-list-create'),
    path('api/users/create/', UserCreateView.as_view(), name='user-list-create'),
    path('api/chats/', ChatsList.as_view(), name='chat-list'),
    path('api/messages/create/', ChatMessageCreate.as_view(), name='message-create'),
    path('api/send-telegram-message/', SendTelegramMessageView.as_view(), name='send_telegram_message'),

    # Add more URL patterns as needed
]