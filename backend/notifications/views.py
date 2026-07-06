from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import time
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def poll_notifications(request):
    """
    Standard endpoint for notifications.
    Checks the database for unread notifications and returns them immediately.
    """
    # Check for unread notifications that are ready to be shown (created_at <= now).
    # This clever trick allows us to schedule future reminders without a Celery background worker!
    unread = Notification.objects.filter(user=request.user, is_read=False, created_at__lte=timezone.now())
    
    if unread.exists():
        serializer = NotificationSerializer(unread, many=True)
        return Response(serializer.data)
        
    return Response([])

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_read(request):
    """
    Endpoint for the frontend to mark notifications as read.
    """
    notification_ids = request.data.get('ids', [])
    Notification.objects.filter(user=request.user, id__in=notification_ids).update(is_read=True)
    return Response({"status": "success"})
