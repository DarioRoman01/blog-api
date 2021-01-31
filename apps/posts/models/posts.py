"""Post models."""

# Django
from django.db import models

# Models
from apps.users.models import User, Profile

class Post(models.Model):
    """Post model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile =  models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='posts/pictures')

    resume = models.CharField(max_length=255)

    like = models.ManyToManyField(User, related_name='like')
    likes = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return user and title."""
        return '{} by @ {}'.format(self.title, self.user.username)

