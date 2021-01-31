"""Coments models."""

# Django
from django.db import models

# Models
from apps.users.models import User, Profile
from apps.posts.models import Post

class Comment(models.Model):
    """Comments model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    content = models.CharField(max_length=255)

    def __str__(self):
        return 'comment by @{}'.format(self.user.username)