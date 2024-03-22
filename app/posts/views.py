"""
Views for the post API.
"""
from rest_framework import generics, authentication, permissions
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

# from django.shortcuts import get_object_or_404
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from core.models import Post, Followship
from user.serializers import OwnerSerializer
from posts.serializers import (
    PostDetailSerializer,
    PostSerializer
)
from posts.signals import post_liked_signal


class CreatePostView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = PostDetailSerializer
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """I wanted to do some stuff with serializer.data here"""

        post = Post.objects.create(owner=request.user,
                                   content=request.data['content'])
        post.save()
        cache.delete("list_posts_view")
        cache.delete("list_my_posts_view")
        return Response(self.serializer_class(post).data,
                        status=status.HTTP_201_CREATED)


create_post_view = CreatePostView.as_view()


# @method_decorator(cache_page(60 * 1), name='dispatch')
class listPostsView(generics.ListAPIView):
    """Show the user profile"""

    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_cache_key(self, *args, **kwargs):
        # Generate a custom cache key based on the request's URL, 
        # query parameters, etc.
        print(f"custom_cache_key:{self.request.get_full_path()}")
        return f"custom_cache_key:{self.request.get_full_path()}"

    # Cache the page for 15 minutes
    @method_decorator(cache_page(60 * 2, key_prefix=''))
    def dispatch(self, *args, **kwargs):
        print(f"custom_cache_key:{self.request.get_full_path()}")
        return super().dispatch(*args, **kwargs)


list_posts_view = listPostsView.as_view()


class ManagePostView(generics.RetrieveUpdateDestroyAPIView):
    """"Manage the user Posts."""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def retrieve(self, request, pk=None):
        cached_post = cache.get(f'post_{pk}')
        if cached_post:
            if cached_post['owner'] == OwnerSerializer(request.user).data:
                return Response(data=cached_post,
                                status=status.HTTP_200_OK)
            if Followship.objects.filter(
                following__name=cached_post['owner']['name']).filter(
                    follower__name=request.user.name):
                return Response(data=cached_post,
                                status=status.HTTP_200_OK)

            return Response(status=status.HTTP_403_FORBIDDEN)

        qs = self.queryset.filter(pk=pk)
        if qs.exists():
            post_owner = qs.first().owner
            is_user_friends = Followship.objects.filter(
                following__name=post_owner.name).filter(
                    follower__name=request.user.name
                )
            qs = qs.filter(owner=request.user)
            if qs.exists() or is_user_friends:
                if not qs:
                    qs = self.queryset.filter(pk=pk)
                item = self.serializer_class(qs.first())
                cache.set(f'post_{pk}', item.data, timeout=60*5)
                return Response(data=item.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None, *args, **kwargs):

        cached_post = cache.get(f'post_{pk}')
        if cached_post:
            if cached_post['owner'] == OwnerSerializer(request.user).data:
                cache.delete(f'post_{pk}')
                cache.delete("list_posts_view")
                cache.delete("list_my_posts_view")
                return self.update(request, *args, **kwargs)

        qs = self.queryset.filter(pk=pk)
        if qs.exists():
            qs = qs.filter(owner=request.user)
            if qs.exists():
                cache.delete(f'post_{pk}')
                cache.delete("list_posts_view")
                cache.delete("list_my_posts_view")
                return self.update(request, *args, **kwargs)
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None, *args, **kwargs):
        cached_post = cache.get(f'post_{pk}')
        if cached_post:
            if cached_post['owner'] == OwnerSerializer(request.user).data:
                cache.delete(f'post_{pk}')
                cache.delete("list_posts_view")
                cache.delete("list_my_posts_view")
                return self.update(request, *args, **kwargs)

        qs = self.queryset.filter(pk=pk)
        if qs.exists():
            qs = qs.filter(owner=request.user)
            if qs.exists():
                cache.delete(f'post_{pk}')
                cache.delete("list_posts_view")
                cache.delete("list_my_posts_view")
                return self.update(request, *args, **kwargs)
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None, *args, **kwargs):
        cached_post = cache.get(f'post_{pk}')
        if cached_post:
            if cached_post['owner'] == OwnerSerializer(request.user).data:
                cache.delete(f'post_{pk}')
                cache.delete("list_posts_view")
                cache.delete("list_my_posts_view")
                return self.destroy(request, *args, **kwargs)

        qs = self.queryset.filter(pk=pk)
        if qs.exists():
            qs = qs.filter(owner=request.user)
            if qs.exists():
                cache.delete(f'post_{pk}')
                cache.delete("list_posts_view")
                cache.delete("list_my_posts_view")
                return self.destroy(request, *args, **kwargs)
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_404_NOT_FOUND)


manage_posts_view = ManagePostView.as_view()


class ListOwnedPosts(generics.ListCreateAPIView):
    """List the user's own posts."""
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication, 
                              authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().filter(
            owner=self.request.user).order_by('id')

    def perform_create(self, serializer, **validated_data):
        post = serializer.save(owner=self.request.user)
        post.save()
        return post

    def get_cache_key(self, *args, **kwargs):
        # Generate a custom cache key based on the request's URL,
        # query parameters, etc.
        return f"custom_cache_key:{self.request.get_full_path()}"

    # Cache the page for 15 minutes
    @method_decorator(cache_page(60 * 2, key_prefix=''))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


list_my_posts_view = ListOwnedPosts().as_view()


class LikePostWithID(generics.RetrieveAPIView):
    """Like a post"""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication, 
                              authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def retrieve(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        post = Post.objects.get(pk=pk)

        if post is not None and request.user not in post.liked_users.all():
            post_liked_signal.send(sender=Post, post_id=post.id, user_id= request.user.id,is_like=True) 
            return Response(data=self.serializer_class(post).data,
                            status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)


like_a_post_view = LikePostWithID().as_view()
