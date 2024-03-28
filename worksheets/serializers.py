from rest_framework import serializers
from .models import *


class WorksheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worksheet
        fields = '__all__'
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'