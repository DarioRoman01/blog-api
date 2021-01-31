"""Profiles models."""

# Django
from django.db import models

# Models
from apps.users.models import User

class Profile(models.Model):
    """profile model. Holds users public information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    biography = models.TextField(max_length=500, blank=True)

    picture = models.ImageField(
        'profile image',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    
    # Stats
    followers = models.PositiveIntegerField(
        default=0,
        help_text='counter of the users that follows the user'
    )

    blog_posted = models.PositiveIntegerField(
        default=0,
        help_text='blog_posted is a counter of the post that the user publish'
    )

    def __str__(self):
        return self.user.username

