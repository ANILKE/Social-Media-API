"""
Views for the post API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from core.models import Comment, Post

from django.core.cache import cache
from user.serializers import OwnerSerializer
from comments.serializers import (
    CommentSerializer
)



class CreateCommentView(generics.CreateAPIView):
    """Create a new comment on a post."""
    serializer_class = CommentSerializer
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """crete the comment wrt post ID"""
        if Post.objects.filter(content = request.data['related_post']).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(owner = request.user, content= request.data['content'],related_post=Post.objects.get(id = request.data['related_post']))
        comment.save()
        related_post = Post.objects.get(id = request.data['related_post'])
        related_post.comments.add(comment.id)
        related_post.save()
        return Response(self.serializer_class(comment).data,status=status.HTTP_201_CREATED)
  

create_comment_view = CreateCommentView.as_view()

class ListCommentsView(generics.ListAPIView):
    """List all the comments"""
    
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

list_posts_view = ListCommentsView.as_view()

class ManageCommentView(generics.RetrieveUpdateDestroyAPIView):
    """"Manage the user Comments."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def retrieve(self, request,pk=None):
        cached_comment = cache.get(f'comment_{pk}')
        if cached_comment:
            post_id = cached_comment.related_post
            post_check = check_post_owner_by_id(post_id.id,request.user)
            if cached_comment.owner.id == request.user.id or post_check:
                print('cached')
                return Response(data = self.serializer_class(cached_comment).data, status = status.HTTP_200_OK)
            return Response( status = status.HTTP_403_FORBIDDEN)
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        comment=self.queryset.filter(pk=pk).first()
        post_check = False
        post_id = None
        if comment:
            cache.set(f'comment_{pk}',comment)
            post_id = comment.related_post
            post_check = check_post_owner_by_id(post_id.id,request.user)
        else:
            return Response( status = status.HTTP_404_NOT_FOUND)
        if qs.exists() or post_check:
            qs= self.queryset.filter(pk=pk)
            if qs.exists():
                item = self.serializer_class(qs.first())
                return Response(data = item.data, status = status.HTTP_200_OK)
        return Response( status = status.HTTP_403_FORBIDDEN)

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
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        comment=self.queryset.filter(pk=pk).first()
        post = None
        post_id = None
        if comment:
            post_id = comment.related_post
            post = Post.objects.filter(pk=post_id.id).first()
        else:
            return Response( status = status.HTTP_400_BAD_REQUEST)
        if qs.exists() or (post and post.owner==request.user):
            return self.destroy(request, *args, **kwargs)
        return Response(status = status.HTTP_401_UNAUTHORIZED)

manage_comment_view = ManageCommentView.as_view()

class ListOwnedComments(generics.ListCreateAPIView):
    """List the user's own comments."""
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Comment.objects.all().filter(owner = self.request.user).order_by('id')
    def perform_create(self, serializer,**validated_data):
        post = serializer.save(owner=self.request.user)
        post.save()
        return post
list_my_comments_view = ListOwnedComments().as_view()


class LikeCommentWithID(generics.RetrieveAPIView):
    """Like a comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request,pk=None):
        """Increment likes of comment and add yourselfe to liked_profiles"""
        if pk is None:
            return Response( status = status.HTTP_401_UNAUTHORIZED)
        comment = Comment.objects.get(pk=pk)
        
        if comment is not None and request.user not in comment.liked_users.all():
            comment.likes +=1
            comment.liked_users.add(request.user)
            comment.save()
            qs = self.queryset.filter(pk=pk)
            return Response(data = self.serializer_class(qs.first()).data, status = status.HTTP_200_OK)
        return Response( status = status.HTTP_401_UNAUTHORIZED)
    
like_a_comment_view = LikeCommentWithID().as_view()

def check_post_owner_by_id(post_id,request_owner):
    cached_post  = cache.get(f'post_{post_id}')
    if cached_post:
        print( "post cached")
        if cached_post.owner == request_owner.id:
            return True
        return False
    post = Post.objects.filter(pk=post_id).first()
    if post :
        print('post not cached')
        cache.set(f'post_{post_id}',post)
        if post.owner == request_owner:
            return True
    return False

