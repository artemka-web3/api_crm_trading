from django.urls import path
from .views import ChatMessageListByChatId, ChatMessageCreate, ChatsList, ChatMessageList, UserCreateView, UserListView, SendTelegramMessageView, SetCaptchaTrue, GetCaptchaValue, UnreadMessagesCountView, ResetUnreadMessages


urlpatterns = [
    path('api/messages/', ChatMessageListByChatId.as_view(), name='message-list'),
    path('api/all_messages/', ChatMessageList.as_view(), name='all-message-list'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/create/', UserCreateView.as_view(), name='user-list-create'),
    path('api/chats/', ChatsList.as_view(), name='chat-list'),
    path('api/messages/create/', ChatMessageCreate.as_view(), name='message-create'),
    path('api/send-telegram-message/', SendTelegramMessageView.as_view(), name='send_telegram_message'),
    path('api/set_captcha_true/', SetCaptchaTrue.as_view(), name='set_captcha_true'),
    path('api/get_captcha_value/', GetCaptchaValue.as_view(), name='get_captcha_value'),
    path('api/unread_messages_count/<int:tg_id>/', UnreadMessagesCountView.as_view(), name='unread_messages_count'),
    path('api/read_all/', ResetUnreadMessages.as_view(), name='reset_unread_messages'),

]

    # Add more URL patterns as needed
