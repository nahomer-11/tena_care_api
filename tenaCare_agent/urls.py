from django.urls import path
from .views import ChatSessionListView, MessageListView, SendMessageView

urlpatterns = [
    path('sessions/', ChatSessionListView.as_view()),
    path('sessions/<int:session_id>/messages/', MessageListView.as_view()), 
    path('sessions/<int:session_id>/send/', SendMessageView.as_view()),  
]
