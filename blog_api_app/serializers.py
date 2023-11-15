from rest_framework import serializers
from .models import User, Post, Comment
from .helper import check_email, check_password
from passlib.hash import django_pbkdf2_sha256 as handler


class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if not check_email(value):
            raise serializers.ValidationError('Email not valid!')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value

    def validate_password(self, value):
        check, message = check_password(value)
        if not check:
            raise serializers.ValidationError(message)
        password = handler.hash(value)
        return password
    
    def validate_username(self, value):
        # Check if the email is unique
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email', 'password']
        

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']