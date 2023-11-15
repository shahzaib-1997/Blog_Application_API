from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, max_length=255
    )
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.TextField()
    profile = models.ImageField(upload_to="User/", default="User/dummy.jpg")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    

class UserWhitelistToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Post(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="Blog/", default="Blog/dummy.png")

    def __str__(self):
        return f"{self.user} - {self.title}"


class Comment(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.post}"
