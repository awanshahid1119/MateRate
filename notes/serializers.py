from rest_framework import serializers
from .models import *

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id','user', 'timestamp', 'title', 'content']