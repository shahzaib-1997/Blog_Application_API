from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from passlib.hash import django_pbkdf2_sha256 as handler
from .models import User, Post, Comment, UserWhitelistToken
from .serializers import RegistrationSerializer, PostSerializer, CommentSerializer, LoginSerializer
from .renderers import UserRenderers


class RegisterView(APIView):

    renderer_classes = [UserRenderers]

    def post(self, request):
        szr = RegistrationSerializer(data=request.data)
        szr.is_valid(raise_exception=True)
        validated_data = szr.validated_data
        User.objects.create(**validated_data)
        
        return Response({
            'status': True,
            'msg': 'User registered successfully.',
            },
            status= status.HTTP_201_CREATED
        )


class LoginView(APIView):
    
    renderer_classes = [UserRenderers]

    def post(self, request):
        szr = LoginSerializer(data=request.data)
        szr.is_valid(raise_exception=True)
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.get(email=email)

        if user and handler.verify(password, user.password):
            refresh = RefreshToken.for_user(user.id)
            UserWhitelistToken.objects.create(user_id=user, token=refresh)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)