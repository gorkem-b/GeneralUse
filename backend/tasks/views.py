import datetime
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    Controller for Tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title', '')
        
        # Basic anti-spam
        one_min_ago = timezone.now() - datetime.timedelta(minutes=1)
        if Task.objects.filter(user=self.request.user, title=title, created_at__gte=one_min_ago).exists():
            raise ValidationError("Duplicate submission detected.")
            
        serializer.save(user=self.request.user)
