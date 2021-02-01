"""Comments serializers."""

# Rest framework
from rest_framework import serializers

# Models 
from apps.posts.models import Comment

# Serializers
from apps.users.serializers import ProfileModelSerializer

class CommentModelSerializer(serializers.ModelSerializer):
    """Comment model serializer."""
    profile = ProfileModelSerializer(read_only=True)
    
    class Meta:
        """Meta class."""
        model = Comment
        fields = (
            'content',
            'profile'
        )


class AddCommentSerializer(serializers.Serializer):

    content = serializers.CharField(max_length=255)

    def create(self, validated_data):
        """Handle comment creation."""

        user = self.context['request'].user
        profile = self.context['request'].user.profile
        post = self.context['post']

        comment = Comment.objects.create(
            **validated_data,
            user=user,
            profile=profile,
            post=post
        )

        return comment
