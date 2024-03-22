"""
Views for the user API.
""" 
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .mixins import SelfUserPermissionMixin

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    ProfileSerialier,
)
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """"Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
    def get_cache_key(self, *args, **kwargs):
        # Generate a custom cache key based on the request's URL, query parameters, etc.
        return f"custom_cache_key:{self.request.get_full_path()}"

    @method_decorator(cache_page(60 * 2, key_prefix=''))  # Cache the page for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
class ShowProfileView(SelfUserPermissionMixin,generics.RetrieveUpdateAPIView):
    """Show the user profile"""
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerialier
    lookup_field = 'pk'
    def get_cache_key(self, *args, **kwargs):
        # Generate a custom cache key based on the request's URL, query parameters, etc.
        return f"custom_cache_key:{self.request.get_full_path()}"

    @method_decorator(cache_page(60 * 2, key_prefix=''))  # Cache the page for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

