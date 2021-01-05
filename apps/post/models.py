from django.db import models

from apps.user_profile.models import UserProfile


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    author = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(UserProfile, related_name='post_like')
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_number_of_likes(self):
        return self.likes.count()
