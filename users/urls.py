from django.urls import path
from .views import RegisterView, LoginView
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('token/', obtain_auth_token), 
]
