# urls.py
from django.urls import path
from .views import (
    ChatSessionListView,
    CreateChatSessionView,
    MessageListView,
    SendMessageView,
    ClearChatHistoryView
)

urlpatterns = [
    path('sessions/', ChatSessionListView.as_view()),
    path('sessions/create/', CreateChatSessionView.as_view()),
    path('sessions/<int:session_id>/messages/', MessageListView.as_view()),
    path('sessions/<int:session_id>/send/', SendMessageView.as_view()),
    path('sessions/clear-history/', ClearChatHistoryView.as_view(), name='clear_chat_history'),
]
