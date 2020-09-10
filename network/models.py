from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Blogpost(models.Model):
    username = models.CharField(max_length=64)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

class Followinfo(models.Model):
    username = models.CharField(max_length=64)
    follower = models.CharField(max_length=64)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.username,
            "follower": self.follower
        }

class Like(models.Model):
    postid = models.IntegerField()
    likedby = models.CharField(max_length=64)
    likes = models.IntegerField()

    def serialize(self):
        return {
            "id": self.postid,
            "likedby": self.likedby,
            "likes": self.likes
        }