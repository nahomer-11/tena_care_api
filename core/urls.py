from .views import RemediesListView, RemediesDetailView, HealthTipsListView, FirstAidListView
from django.urls import path 

urlpatterns = [
    path('remedies/', RemediesListView.as_view(), name='remedies-list'),
    path('remedies/<int:id>/', RemediesDetailView.as_view(), name='remedies-detail'),
    path('health-tips/', HealthTipsListView.as_view(), name='health-tips-list'),
    path('first-aid/', FirstAidListView.as_view(), name='first-aid-list'),
]