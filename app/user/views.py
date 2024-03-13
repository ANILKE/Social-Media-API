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

class ShowProfileView(SelfUserPermissionMixin,generics.RetrieveUpdateAPIView):
    """Show the user profile"""
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerialier
    lookup_field = 'pk'

