"""Posts serializers."""

# Rest framework
from rest_framework import serializers

# Models
from apps.posts.models import Post

# Serializers
from apps.users.serializers import ProfileModelSerializer
from apps.posts.serializers.comments import CommentModelSerializer


class PostModelSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    profile = ProfileModelSerializer(read_only=True)
    comments = CommentModelSerializer(read_only=True, many=True)

    class Meta:
        """Meta class."""
        model = Post
        fields = (
            'title',
            'picture',
            'resume',
            'likes',
            'profile',
            'comments',
        )
        read_only_fields = (
            'likes',
        )

class CreatePostSerializer(serializers.Serializer):
    """Create post serializer."""

    title = serializers.CharField(max_length=50)
    picture = serializers.ImageField()
    resume = serializers.CharField(max_length=255)

    def create(self, validated_data):
        """Handle post creation."""

        user = self.context['request'].user
        profile = self.context['request'].user.profile
        post = Post.objects.create(**validated_data, user=user, profile=profile)

        return post

        
