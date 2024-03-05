"""
Views for Friendships.
"""

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from .mixins import SelfUserPermissionMixin

from core.models import Followship

from follower import serializers


class FollowerViewSet(viewsets.ModelViewSet):
    """View for manage Firendships APIs"""
    serializer_class = serializers.FriendshipDetailSerializer
    queryset = Followship.objects.all()
    lookup_field = 'pk' 
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer, **extra_fields):
        """Create a new friendship."""
        serializer.save(follower = self.request.user)
        
    def destroy(self,request, pk =None):
        """Delete the followship"""
        item = get_object_or_404(self.queryset, pk=pk)
        if item.following == request.user or item.follower == request.user:
            item.delete()  
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status= status.HTTP_401_UNAUTHORIZED)
        
    def update(self,serializer, pk =None):
        """ Block pdate a followship"""
        
        self.permission_classes = [IsAdminUser]
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)   
    def partial_update(self,request, pk =None, **fields):
        """ Block pdate a followship"""
        self.permission_classes = [IsAdminUser]
        return Response(status= status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, pk=None):
        """Retrieve a friendship with pk."""
        item = get_object_or_404(self.queryset, pk=pk)
        if(item.following == request.user or item.follower == request.user):
            serializer = self.serializer_class(item)
            return Response(serializer.data)
        return Response(status= status.HTTP_401_UNAUTHORIZED)
            
            
    def get_queryset(self):
        if self.request.GET.get('id') is None:
            return self.queryset.filter(following = self.request.user).order_by('follower')
        return self.queryset.filter(following = self.request.GET.get('id')).order_by('follower')

    def get_serialier_class(self):
        if self.action == 'list':
            return serializers.FriendshipSerializer
        return self.serializer_class
    
     