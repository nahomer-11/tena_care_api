from .models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_active', 'is_staff']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_full_name(self, value):
        if not value:
            raise serializers.ValidationError("Full name is required.")
        return value
