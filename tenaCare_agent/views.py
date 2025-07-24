from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from tenaCare_agent.agent import agent 


class CreateChatSessionView(CreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatSessionListView(ListAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        return Message.objects.filter(session__id=session_id, session__user=self.request.user)


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        content = request.data.get('content')
        user = request.user

        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            session = ChatSession.objects.get(id=session_id, user=user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Chat session not found."}, status=status.HTTP_403_FORBIDDEN)

        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_messages = Message.objects.filter(
            session__user=user,
            sender='user',
            time_stamp__gte=today_start
        ).count()

        if today_messages >= 10:
            
            return Response({"error": "You have reached your daily limit of 10 messages."}, status=429)

        
        user_message = Message.objects.create(session=session, sender='user', content=content)

        
        try:
            agent_result = agent.invoke({"input": content})
            ai_response = (
                agent_result.get("output")
                if isinstance(agent_result, dict)
                else str(agent_result)
            )
        except Exception as e:
            print(f"[TenaCare ERROR] AI agent failed: {str(e)}")
            
            user_message.delete()
            return Response(
                {"error": "Sorry, the AI failed to respond. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        
        ai_message = Message.objects.create(session=session, sender='ai', content=ai_response)

        return Response({
            "user_message": MessageSerializer(user_message).data,
            "ai_message": MessageSerializer(ai_message).data
        }, status=status.HTTP_201_CREATED)

class ClearChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        ChatSession.objects.filter(user=user).delete()  
        return Response({"message": "Chat history cleared."}, status=status.HTTP_204_NO_CONTENT)
