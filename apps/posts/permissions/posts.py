"""Post permissions."""

# Rest framework
from rest_framework.permissions import BasePermission

# Models
from apps.posts.models import Post

class IsPostOwner(BasePermission):
    """Allow access only to post owner."""

    def has_object_permission(self, request, view, obj):
        """Verify user is the creator obj."""
        try:
            Post.objects.get(user=request.user)

        except Post.DoesNotExist:
            return False
            
        return True