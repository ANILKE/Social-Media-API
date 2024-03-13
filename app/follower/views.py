"""
Views for Friendships.
"""
import json
from rest_framework import viewsets, status,renderers
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.core.cache import cache
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
    #renderer_classes = [renderers.TemplateHTMLRenderer]
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer, **extra_fields):
        """Create a new friendship."""
        serializer.save(follower = self.request.user)
        
    def destroy(self,request, pk =None):
        """Delete the followship"""
        item = get_object_or_404(self.queryset, pk=pk)
        if item.following == request.user or item.follower == request.user:
            cache.delete(f'follow_query_set_{item.following.id}')
            item.delete()  
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status= status.HTTP_403_FORBIDDEN)

    def list(self,request, pk =None):
        """List followships"""
        qs= self.get_queryset()
        serialized = self.serializer_class(qs,many = True)
        # serializer_return_list = serialized.data
        # converted_data = []
        # for ordered_dict in serializer_return_list:
        #     converted_data.append(dict(ordered_dict))
        # result = {}
        # result['followers'] = converted_data,
        # id = request.GET.get('id')
        # if id:
        #     user = UserSerializer(get_user_model().objects.filter(pk=id).first()).data
        #     result['user'] = {'id':id,'name':user['name'],'email':user['email']}
        
            
        if qs.exists():
            return Response(data = serialized.data,status= status.HTTP_200_OK)
        if self.queryset.exists():
            return Response(status= status.HTTP_403_FORBIDDEN)

        return Response(status= status.HTTP_404_NOT_FOUND)
        
    def update(self,serializer, pk =None):
        """ Block pdate a followship"""
        
        self.permission_classes = [IsAdminUser]
        
        return Response(status=status.HTTP_403_FORBIDDEN)   
    def partial_update(self,request, pk =None, **fields):
        """ Block pdate a followship"""
        self.permission_classes = [IsAdminUser]
        return Response(status= status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, pk=None):
        """Retrieve a friendship with pk."""
        item = get_object_or_404(self.queryset, pk=pk)
        if(item.following == request.user or item.follower == request.user):
            serializer = self.serializer_class(item,context={'request': request})
            return Response(serializer.data,)
        
        return Response(status= status.HTTP_403_FORBIDDEN)
            
            
    def get_queryset(self):
        
        if self.request.GET.get('id') is None:
            cached_qs = cache.get(f'follow_query_set_{self.request.user.id}')
            if cached_qs:
                print("follower list cached for self")
                return cached_qs
            qs = self.queryset.filter(following = self.request.user).order_by('follower')  
            cache.set(f'follow_query_set_{self.request.user.id}',qs, timeout=60*5)
            print("connot catch self follower list")
            return qs  
        cached_qs = cache.get(f"follow_query_set_{self.request.GET.get('id')}") 
        if cached_qs:
                print("follower list cached for param")
                if(self.request.GET.get('id') == str(self.request.user.id)):
                    return cached_qs
                if cached_qs.filter(follower = self.request.user).exists():
                    return cached_qs
                return self.queryset.none()
        qs = self.queryset.filter(following = self.request.GET.get('id')).order_by('follower')
        print("connot catch param follower list")
        
        if(self.request.GET.get('id') == str(self.request.user.id)):
            cache.set(f'follow_query_set_{self.request.user.id}',q, timeout=60*5)
            print("set catch param self follower list")
            
            return qs
        if qs.filter(follower = self.request.user).exists():
            cache.set(f"follow_query_set_{self.request.GET.get('id')}",qs, timeout=60*5)
            print("set catch param follower list")
            return qs
        return self.queryset.none() #Response(status= status.HTTP_401_UNAUTHORIZED) 

    def get_serialier_class(self):
        if self.action == 'list':
            return serializers.FriendshipSerializer
        return self.serializer_class