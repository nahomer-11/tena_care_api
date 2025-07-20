from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Remedies, HealthTips, FirstAid
from .serializers import RemediesSerializer, HealthTipsSerializer, FirstAidSerializer


# Create your views here.
class RemediesListView(ListAPIView):
    queryset = Remedies.objects.all()
    serializer_class = RemediesSerializer

class RemediesDetailView(RetrieveAPIView):
    queryset = Remedies.objects.all()
    serializer_class = RemediesSerializer
    lookup_field = 'id'

class HealthTipsListView(ListAPIView):
    queryset = HealthTips.objects.all()
    serializer_class = HealthTipsSerializer
    
class FirstAidListView(ListAPIView):
    queryset = FirstAid.objects.all()
    serializer_class = FirstAidSerializer