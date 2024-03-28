from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class NoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Note
        fields = ['user', 'timestamp', 'title', 'content', 'educator_feedback', 'resources']