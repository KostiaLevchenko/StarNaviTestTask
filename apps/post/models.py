from django.db import models

from apps.user_profile.models import UserProfile


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    author = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(UserProfile, through='Like', related_name='post')
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_number_of_likes(self):
        return self.likes.count()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
