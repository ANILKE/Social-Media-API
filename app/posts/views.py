"""
Views for the post API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from core.models import Post

from posts.serializers import (
    PostDetailSerializer,
    PostSerializer
)



class CreatePostView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = PostDetailSerializer
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

create_post_view = CreatePostView.as_view()

class listPostsView(generics.ListAPIView):
    """Show the user profile"""
    
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

list_posts_view = listPostsView.as_view()

class ManagePostView(generics.RetrieveUpdateDestroyAPIView):
    """"Manage the user Posts."""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def retrieve(self, request,pk=None):
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        if qs.exists():
            item = self.serializer_class(qs.first())
            return Response(data = item.data, status = status.HTTP_200_OK)
        return Response( status = status.HTTP_401_UNAUTHORIZED)

    def put(self, request,pk=None, *args, **kwargs):
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        if qs.exists():
            return self.update(request, *args, **kwargs)
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    def patch(self, request,pk=None, *args, **kwargs):
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        if qs.exists():
            return self.update(request, *args, **kwargs)
        return Response(status = status.HTTP_401_UNAUTHORIZED)
    def delete(self, request,pk=None, *args, **kwargs):
        print(pk)
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        print(qs)
        if qs.exists():
            return self.destroy(request, *args, **kwargs)
        return Response(status = status.HTTP_401_UNAUTHORIZED)

manage_posts_view = ManagePostView.as_view()

class ListOwnedPosts(generics.ListCreateAPIView):
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all().filter(owner = self.request.user).order_by('id')
    def perform_create(self, serializer,**validated_data):
        post = serializer.save(owner=self.request.user)
        post.save()
        return post
list_my_posts_view = ListOwnedPosts().as_view()

class LikePostWithID(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request,pk=None):
        if pk is None:
            return Response( status = status.HTTP_401_UNAUTHORIZED)
        post = Post.objects.get(pk=pk)
        
        if post is not None and request.user not in post.liked_users:
            post.likes +=1
            post.save()
            qs = self.queryset.filter(pk=pk)
            return Response(data = self.serializer_class(qs.first()).data, status = status.HTTP_200_OK)
        return Response( status = status.HTTP_401_UNAUTHORIZED)
    
like_a_post_view = LikePostWithID().as_view()


