import uuid
from django.db import models
from django.contrib.auth.models import User

class ActiveManager(models.Manager):
    """
    Custom manager that automatically filters out soft-deleted records from queries.
    This enforces data integrity by keeping 'deleted' items in the database 
    without showing them to the user.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Task(models.Model):
    """
    Model for the Task Scheduler Engine.
    Represents a To-Do list item for a user.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    due_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_deleted = models.BooleanField(default=False)
    
    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.title} ({self.status})"
