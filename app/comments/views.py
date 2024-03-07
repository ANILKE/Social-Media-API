"""
Views for the post API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from core.models import Comment, Post
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
        if not Post.objects.filter(pk=request.data['related_post_id']).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(owner = request.user, content= request.data['content'],related_post_id=request.data['related_post_id'])
        comment.save()
        related_post = Post.objects.get(id=request.data['related_post_id'])
        related_post.comments.add(comment)
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
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        comment=self.queryset.filter(pk=pk).first()
        post = None
        post_id = None
        if comment:
            post_id = comment.related_post_id
            post = Post.objects.filter(pk=post_id).first()
        else:
            return Response( status = status.HTTP_400_BAD_REQUEST)
        if qs.exists() or(post and post.owner==request.user):
            qs= self.queryset.filter(pk=pk)
            if qs.exists():
                print(request)
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
        qs = self.queryset.filter(owner = request.user).filter(pk=pk)
        comment=self.queryset.filter(pk=pk).first()
        post = None
        post_id = None
        if comment:
            post_id = comment.related_post_id
            post = Post.objects.filter(pk=post_id).first()
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


class LikePostWithID(generics.RetrieveAPIView):
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
    
like_a_post_view = LikePostWithID().as_view()


