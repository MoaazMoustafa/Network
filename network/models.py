from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


class User(AbstractUser):
    pass


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=SET_NULL, null=True, related_name="user_followers")
    followed = models.ForeignKey(
        User, on_delete=SET_NULL, null=True, related_name="user_following")

    def __str__(self):
        return f'{self.follower.username} has followed {self.followed.username}'

    class Meta:
        unique_together = (('follower', 'followed'),)


class Post(models.Model):
    post = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='creator')
    time = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(
        'User', null=True, blank=True, related_name='likes')

    def __str__(self):
        return self.post
