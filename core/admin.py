from django.contrib import admin
from .models import Remedies, HealthTips , FirstAid # Import your models

# Register your models here.
admin.site.register([Remedies, HealthTips, FirstAid])  # Register your models here