from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    BlogPostView,
    PostCommentView
    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-blog-post/', BlogPostView.as_view(), name='blog-post'),
    path('comment/', PostCommentView.as_view(), name='post-comment'),
    
]