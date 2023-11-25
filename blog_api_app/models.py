import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=255
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    email = models.EmailField(max_length=255, unique=True)
    profile = models.ImageField(upload_to="User/", default="User/dummy.jpg")

    def __str__(self):
        return self.email


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="Blog/", default="Blog/dummy.png")

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
