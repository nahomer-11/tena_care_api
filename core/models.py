from django.db import models

# Create your models here.
class Remedies(models.Model):
    ImageURL = models.URLField(max_length=200)
    Title = models.CharField(max_length=100)
    Tag = models.CharField(max_length=50)
    Stars = models.IntegerField(default=0)
    Date = models.DateTimeField(auto_now_add=True)
    Description = models.TextField(max_length=500)
    Ingredients = models.CharField(max_length=400)
    Instructions = models.TextField(max_length=4000)
    HowToUse = models.CharField(max_length=300)
    Precautions = models.CharField(max_length=300)
    
    def __str__(self):
        return self.Title
    
class HealthTips(models.Model):
    ImageURL = models.URLField(max_length=200)
    Title = models.CharField(max_length=100)
    Tip = models.TextField(max_length=500)
    Tag = models.CharField(max_length=50)
    Date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Title
    
class FirstAid(models.Model):
    ImageURL = models.URLField(max_length=200)
    Title = models.CharField(max_length=100)
    Warning = models.TextField(max_length=2000)
    Instructions = models.TextField(max_length=4000)
    
    def __str__(self):
        return self.Title

