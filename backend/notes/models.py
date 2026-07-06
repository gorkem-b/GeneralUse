import uuid
from django.db import models
from django.contrib.auth.models import User

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Note(models.Model):
    """
    Model for the Notes Document Engine.
    Represents a plaintext note created by a specific user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    
    is_archived = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_deleted = models.BooleanField(default=False)
    objects = ActiveManager()
    all_objects = models.Manager()
