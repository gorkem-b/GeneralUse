import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    """
    Model for the In-App Notification Engine.
    Replaces the legacy background email system.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    # Track whether the user has seen this notification on the frontend
    is_read = models.BooleanField(default=False)
    
    # Default to now, but can be set to a future date to act as a scheduled reminder!
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
