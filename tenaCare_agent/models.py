from django.db import models
from django.conf import settings

# Create your models here.
class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ChatSession {self.id} for {self.user.full_name}"
    
class Message(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=50, choices=(('user', 'User'), ('ai', 'Ai'))) # 'user' or 'agent'
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"
    