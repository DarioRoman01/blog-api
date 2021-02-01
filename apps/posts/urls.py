"""posts urls."""

# Django
from django.urls import path, include

# Rest framework
from rest_framework.routers import DefaultRouter

# views
from apps.posts import views

# Router init
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls))
]