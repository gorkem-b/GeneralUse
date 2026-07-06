import datetime
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content', '')
        
        if content.strip():  # Only check for duplication on non-empty content
            one_min_ago = timezone.now() - datetime.timedelta(minutes=1)
            if Note.objects.filter(user=self.request.user, content=content, created_at__gte=one_min_ago).exists():
                raise ValidationError("Duplicate submission detected.")
            
        serializer.save(user=self.request.user)

