import datetime
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer
from notifications.models import Notification

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).order_by('event_timestamp')

    def perform_create(self, serializer):
        event_name = serializer.validated_data.get('event_name', '')
        description = serializer.validated_data.get('description')
        event_timestamp = serializer.validated_data.get('event_timestamp')
        
        one_min_ago = timezone.now() - datetime.timedelta(minutes=1)
        if Event.objects.filter(user=self.request.user, event_name=event_name, created_at__gte=one_min_ago).exists():
            raise ValidationError("Duplicate submission detected.")
            
        event = serializer.save(user=self.request.user)
        
        Notification.objects.create(
            user=self.request.user,
            title=f"Reminder: {event_name}",
            message=description or f"It's time for your event: {event_name}",
            created_at=event_timestamp
        )

