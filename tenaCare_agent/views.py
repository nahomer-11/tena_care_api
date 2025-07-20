# The above code defines views for creating chat sessions, listing sessions and messages, and sending
# messages with limits in a Django REST framework API.
# views.py
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from tenaCare_agent.agent import agent  # your AI logic

# ✅ Create a new session
class CreateChatSessionView(CreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ✅ List sessions for current user
class ChatSessionListView(ListAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

# ✅ List messages for session (user must own the session)
class MessageListView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        return Message.objects.filter(session__id=session_id, session__user=self.request.user)

# ✅ Send message (limit: 10 per day per user)
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        content = request.data.get('content')
        user = request.user

        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check session ownership
        try:
            session = ChatSession.objects.get(id=session_id, user=user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Chat session not found."}, status=status.HTTP_403_FORBIDDEN)

        # Count messages sent by user today
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_messages = Message.objects.filter(
            session__user=user,
            sender='user',
            time_stamp__gte=today_start
        ).count()

        if today_messages >= 10:
            # Don't save new message, don't call AI
            return Response({"error": "You have reached your daily limit of 10 messages."}, status=429)

        # Save user message first
        user_message = Message.objects.create(session=session, sender='user', content=content)

        # Try to generate AI response
        try:
            agent_result = agent.invoke({"input": content})
            ai_response = (
                agent_result.get("output")
                if isinstance(agent_result, dict)
                else str(agent_result)
            )
        except Exception as e:
            print(f"[TenaCare ERROR] AI agent failed: {str(e)}")
            # Since AI response failed, delete the user message we just saved
            user_message.delete()
            return Response(
                {"error": "Sorry, the AI failed to respond. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Save AI message only if AI response succeeded
        ai_message = Message.objects.create(session=session, sender='ai', content=ai_response)

        return Response({
            "user_message": MessageSerializer(user_message).data,
            "ai_message": MessageSerializer(ai_message).data
        }, status=status.HTTP_201_CREATED)

