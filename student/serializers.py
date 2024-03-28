from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import Student, Classroom


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = ('name',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class ChangeUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirm_username = serializers.CharField()

    def validate(self, data):
        user = self.context.get("request").user
        if data['username'] != data['confirm_username']:
            raise exceptions.ParseError("Usernames do not match")
        else:
            return data

    def create(self, validated_data):
        user = self.context.get('request').user
        user.username = validated_data['username']
        user.save()
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['password'] == data['confirm_password']:
            user = self.context.get("request").user
            if user.check_password(data['current_password']):
                return data
            else:
                raise exceptions.ParseError("Incorrent Password")
        else:
            raise exceptions.ParseError("Passwords do not match")

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['standard', 'email', 'premium_user', 'contact_no',
                  'guardian_name', 'guardian_contact', 'guardian_address', 'school_name']
        
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        fields = ['email', 'password']