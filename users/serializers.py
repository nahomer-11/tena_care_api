from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_active', 'is_staff']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_full_name(self, value):
        if not value:
            raise serializers.ValidationError("Full name is required.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
