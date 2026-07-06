import uuid
from django.db import models
from django.contrib.auth.models import User

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Event(models.Model):
    """
    Model for the Event Reminder Scheduler.
    Represents a scheduled event that requires a background email reminder.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    
    event_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    event_timestamp = models.DateTimeField()
    reminder_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_deleted = models.BooleanField(default=False)
    objects = ActiveManager()
    all_objects = models.Manager()
