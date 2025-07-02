from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ChatSessionListView(ListAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

class MessageListView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        return Message.objects.filter(session__id=session_id)
    

class SendMessageView(APIView):
    def post(self, request, session_id):
        content = request.data.get('content')
        
        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Chat session not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user_message = Message.objects.create(
            session=session,
            sender='user',
            content = content
        )
        
        ai_reponse = f"Dummy AI response to: {content}" 
        
        ai_message = Message.objects.create(
            session=session,
            content=ai_reponse,
            sender='ai'
        )
        
        return Response({
            "user_message": MessageSerializer(user_message).data,
            "ai_message": MessageSerializer(ai_message).data
        }, status=status.HTTP_201_CREATED)