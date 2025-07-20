# urls.py
from django.urls import path
from .views import (
    ChatSessionListView,
    CreateChatSessionView,
    MessageListView,
    SendMessageView
)

urlpatterns = [
    path('sessions/', ChatSessionListView.as_view()),
    path('sessions/create/', CreateChatSessionView.as_view()),
    path('sessions/<int:session_id>/messages/', MessageListView.as_view()),
    path('sessions/<int:session_id>/send/', SendMessageView.as_view()),
]
