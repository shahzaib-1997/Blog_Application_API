from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from passlib.hash import django_pbkdf2_sha256 as handler
from .models import User, Post, Comment
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

        user = User.objects.filter(email=email).first()

        if user:
            if handler.verify(password, user.password):
                token , created = Token.objects.get_or_create(user=user)
                return Response({
                    'status' : True,
                    'msg': 'Login successfully!',
                    'token': token.key,
                    'user_id': str(user.id)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status' : False,
                    'error': 'Incorrect Password!'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status' : False,
                'error': 'Email not correct!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        

class BlogPostView(APIView):
    renderer_classes = [UserRenderers]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(user=request.user)
        return Response({            
            'status': True,
            'msg': 'Blog post created successfully.',
            'post_id': str(post.id)
            }, status=status.HTTP_201_CREATED)


class PostCommentView(APIView):
    renderer_classes = [UserRenderers]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({
                'status' : False,
                'error': 'Post not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(user=request.user, post=post)
        return Response({
            'status': True,
            'msg': 'Comment posted successfully.',
            'comment_id': str(comment.id)
            }, status=status.HTTP_201_CREATED)
