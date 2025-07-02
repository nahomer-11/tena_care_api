from .models import ChatSession, Message
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'session', 'sender', 'content', 'time_stamp']
        read_only_fields = ['id', 'time_stamp']
        
    def validate_sender(self, value):
        if value not in ['user', 'ai']:
            raise serializers.ValidationError("Sender must be either 'user' or 'ai'.")
        return value