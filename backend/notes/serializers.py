from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    content = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
