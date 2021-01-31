"""Profiles serializers."""

# Rest framework
from rest_framework import serializers

# Models
from apps.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""
        model = Profile
        fields = (
            'biography',
            'picture',
            'followers',
            'blog_posted'
        )
        read_only_fields = (
            'followers',
            'blog_posted'
        )  