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
        user = request.user
        content = request.data.get('content')

        # Try to get the session, or create it if not found
        session, created = ChatSession.objects.get_or_create(
            id=session_id,
            defaults={'user': user}
        )

        # If it existed but belonged to another user, deny access
        if not created and session.user != user:
            return Response({"error": "You do not have access to this chat session."}, status=status.HTTP_403_FORBIDDEN)

        # Create message
        message = Message.objects.create(
            session=session,
            sender='user',
            content=content
        )

        return Response({
            'message': f'Message sent to session {session.id}',
            'session_id': session.id,
            'content': message.content,
            'timestamp': message.time_stamp
        }, status=status.HTTP_201_CREATED)
