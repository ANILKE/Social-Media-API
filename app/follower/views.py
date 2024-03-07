"""
Views for Friendships.
"""
import json
from rest_framework import viewsets, status,renderers
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .mixins import SelfUserPermissionMixin

from core.models import Followship
from user.serializers import UserSerializer
from follower import serializers

"""Bosken list unauth dönüyo düzelt"""
class FollowerViewSet(viewsets.ModelViewSet):
    """View for manage Firendships APIs"""
    serializer_class = serializers.FriendshipDetailSerializer
    queryset = Followship.objects.all()
    lookup_field = 'pk' 
    renderer_classes = [renderers.TemplateHTMLRenderer]
    
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
            return Response(status=status.HTTP_204_NO_CONTENT, template_name='basic.html')

        return Response(status= status.HTTP_401_UNAUTHORIZED, template_name='unauthorized.html')

    def list(self,request, pk =None):
        """List followships"""
        qs= self.get_queryset()
        serialized = self.serializer_class(qs,many = True)
        serializer_return_list = serialized.data
        converted_data = []
        for ordered_dict in serializer_return_list:
            print(dict(ordered_dict))
            converted_data.append(dict(ordered_dict))
        result = {}
        result['followers'] = converted_data,
        id = request.GET.get('id')
        if id:
            print(id)
            user = UserSerializer(get_user_model().objects.filter(pk=id).first()).data
            print(user)
            result['user'] = {'id':id,'name':user['name'],'email':user['email']}
        
            
        if qs.exists():
            return Response(data = result,status= status.HTTP_200_OK, template_name='basic.html')

        return Response(status= status.HTTP_401_UNAUTHORIZED, template_name='unauthorized.html')
        
    def update(self,serializer, pk =None):
        """ Block pdate a followship"""
        
        self.permission_classes = [IsAdminUser]
        
        return Response(status=status.HTTP_401_UNAUTHORIZED, template_name='basic.html')   
    def partial_update(self,request, pk =None, **fields):
        """ Block pdate a followship"""
        self.permission_classes = [IsAdminUser]
        return Response(status= status.HTTP_401_UNAUTHORIZED, template_name='unauthorized.html')
    
    def retrieve(self, request, pk=None):
        """Retrieve a friendship with pk."""
        item = get_object_or_404(self.queryset, pk=pk)
        if(item.following == request.user or item.follower == request.user):
            serializer = self.serializer_class(item,context={'request': request})
            print(serializer.data)
            return Response(serializer.data, template_name='retrieve.html')
        
        return Response(status= status.HTTP_401_UNAUTHORIZED, template_name='unauthorized.html')
            
            
    def get_queryset(self):
        if self.request.GET.get('id') is None:
            return self.queryset.filter(following = self.request.user).order_by('follower')          
        qs = self.queryset.filter(following = self.request.GET.get('id')).order_by('follower')
        if(self.request.GET.get('id') == str(self.request.user.id)):
            return qs
        if qs.filter(follower = self.request.user).exists():
            return qs
        return self.queryset.none() #Response(status= status.HTTP_401_UNAUTHORIZED) 

    def get_serialier_class(self):
        print(self.action)
        if self.action == 'list':
            return serializers.FriendshipSerializer
        return self.serializer_class
    
     