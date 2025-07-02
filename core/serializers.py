from .models import  Remedies, HealthTips, FirstAid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class RemediesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remedies
        fields = '__all__'

class HealthTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthTips
        fields = '__all__'
        
class FirstAidSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstAid
        fields = '__all__'