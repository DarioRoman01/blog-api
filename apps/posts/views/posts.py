"""Posts views."""

# Rest framework
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status, viewsets, mixins

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from apps.posts.permissions import IsPostOwner

# Serializers
from apps.posts.serializers import (
    CommentModelSerializer,
    PostModelSerializer,
    CreatePostSerializer,
    AddCommentSerializer
)

# Models
from apps.posts.models import Post, Comment

class PostViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    """Post view set."""

    serializer_class = PostModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['like', 'retrieve', 'list', 'store']:
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permissions = [IsAuthenticated, IsPostOwner]
        else:
            permissions = [IsAuthenticated]

        return [p() for p in permissions]

    def get_object(self):
        """return specific post."""
        return get_object_or_404(
            Post,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        """Assign querys based on actions."""
        
        queryset = Post.objects.all()

        if self.action in ['like', 'retrieve', 'update', 'partial_update', 'destroy']:
            return queryset.get(pk=self.kwargs['pk'])

        elif self.action == 'list':
            user = self.request.user
            id_list = []
            follow_list = list(user.follow.all())

            for i in follow_list:
                id_list.append(i.id)
            id_list.append(user.id)

            return queryset.filter(user_id__in=id_list)

        return queryset

    @action(detail=False, methods=['POST'])
    def store(self, request):
        """Handle post creation.""" 

        serializer = CreatePostSerializer(context={'request': request}, data=request.data)
        serializer.is_valid()
        post = serializer.save()
        data = PostModelSerializer(post).data

        # Update profile stats
        profile = request.user.profile
        profile.blog_posted += 1
        profile.save()

        return Response(data, status=status.HTTP_201_CREATED)

    
    @action(detail=True, methods=['POST'])
    def comment(self, request, pk):
        """handle comments for posts."""

        post = self.get_object()
        serializer = AddCommentSerializer(
            context={'request': request, 'post': post},
            data=request.data
        )
        serializer.is_valid()
        serializer.save()

        comments = Comment.objects.filter(post=post)

        data = {
            'post': PostModelSerializer(post).data,
            'comments': CommentModelSerializer(comments, many=True).data
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        """Handle likes to post. and post like stats"""

        post = self.get_object()
        liked = False

        if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)
            liked = False
            post.likes -= 1
            post.save()

        else:
            post.like.add(request.user)
            liked = True
            post.likes += 1
            post.save()

        if liked == True:
            message = 'You liked {}'.format(post.title)
        else:
            message = 'You unliked {}'.format(post.title)
        
        comments = Comment.objects.filter(post=post)

        data = {
            'post': PostModelSerializer(post).data,
            'comments': CommentModelSerializer(comments, many=True).data,
            'message': message
        }

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super(PostViewSet, self).retrieve(request, *args, **kwargs)

        post = self.get_object()
        comments = Comment.objects.filter(post=post)

        data = {
            'post': PostModelSerializer(post).data,
            'comments': CommentModelSerializer(comments, many=True).data
        }

        response.data = data

        return response
