"""
Tests for the comments API.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core import models

CREATE_COMMENT_URL = reverse('comments:create')
LIST_MY_COMMENTS_URL = reverse('comments:myComments')
MANAGE_COMMENT_URL = 'http://testserver/api/comments/'
LIKE_COMMENT_URL = 'http://testserver/api/comments/like/'

def create_comment(**params):
    """Create and return a new comment."""
    return models.Comment.objects.create(**params)



class PublicCommentApiTests(TestCase):
    """Test the public features of the comments API."""

    def setUp(self):
        self.client = APIClient()

class PrivateCommentApiTests(TestCase):
    """Test the private features of the comments API."""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.anotheruser = get_user_model().objects.create(
            email='another@example.com',
            password='testpass123',
            name='Test Another',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        
    def test_create_comment_success(self):
        """Test creating a comment is successful."""
        post = models.Post.objects.create(owner=self.user,content='test post.')
        payload = {
            'owner': self.user,
            'content': 'test comment1.',
            'related_post': post.id,
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment = models.Comment.objects.get(content = payload['content'])
        post = models.Post.objects.get(content = post.content)
        self.assertEqual(comment.related_post, post)
        self.assertIn(comment, post.comments.all())

    def test_retrieve_comment_success(self):
        """Test creating a comment is successful."""
        post = models.Post.objects.create(owner=self.user,content='test post.')
        payload = {
            'owner': self.user,
            'content': 'test comment2.',
            'related_post': post.id,
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)
        comment = models.Comment.objects.get(content = payload['content'])
        used_url = MANAGE_COMMENT_URL+str(comment.id)+"/"
        res = self.client.get(used_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], comment.id)
        self.assertEqual(res.data['related_post'], comment.related_post.id)
        self.assertEqual(res.data['content'], comment.content)

    def test_update_comment_success(self):
        """Test put request to a comment is successful."""
        post = models.Post.objects.create(owner=self.user,content='test post.')
        payload = {
            'owner': self.user,
            'content': 'test comment3.',
            'related_post': post.id,
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)
        new_payload = {
            'content': 'test comment123.',
            'related_post': post.id,
        }
        comment = models.Comment.objects.get(content = payload['content'])
        
        used_url = MANAGE_COMMENT_URL+str(comment.id)+"/"
        res = self.client.put(used_url,new_payload)
        
        comment = models.Comment.objects.get(content = new_payload['content'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['owner'], comment.owner)
        self.assertEqual(payload['related_post'], comment.related_post.id)
        self.assertEqual(new_payload['content'], comment.content)
    def test_delete_comment_success(self):
        """Test delete request to a comment is successful."""
        post = models.Post.objects.create(owner=self.user,content='test post.')
        payload = {
            'owner': self.user,
            'content': 'test comment4.',
            'related_post': post.id,
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)
        
        comment = models.Comment.objects.get(content = payload['content'])
        
        used_url = MANAGE_COMMENT_URL+str(comment.id)+"/"
        self.assertTrue(models.Comment.objects.filter(content = payload['content']).exists())
        res = self.client.delete(used_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Comment.objects.filter(content = payload['content']).exists())

    def test_list_own_comment_success(self):
        """Test listing all of owned comments is successful."""
        
        post = models.Post.objects.create(owner=self.user,content='test post.')
        payload1 = {
            'owner': self.user,
            'content': 'test comment5.',
            'related_post': post.id,
        }
        payload2= {
            'owner': self.user,
            'content': 'test comment6.',
            'related_post': post.id,
        }
        payload3= {
            'owner': self.anotheruser,
            'content': 'test comment for other user1.',
            'related_post': post.id,
        }
        res = self.client.post(CREATE_COMMENT_URL, payload1)
        res = self.client.post(CREATE_COMMENT_URL, payload2)
        res = self.client.post(CREATE_COMMENT_URL, payload3)
        
        comment1 = models.Comment.objects.get(content = payload1['content'])
        comment2 = models.Comment.objects.get(content = payload2['content'])
        comment3 = models.Comment.objects.get(content = payload3['content'])
        res = self.client.get(LIST_MY_COMMENTS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for comment in res.data['results']:
            self.assertEqual(self.user.name, comment['owner']['name'])

    def test_like_comment_success(self):
        """Test listing all of owned comments is successful."""
        
        post = models.Post.objects.create(owner=self.user,content='test post.')
        payload = {
            'owner': self.user,
            'content': 'test comment7.',
            'related_post': post.id,
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)

        
        comment = models.Comment.objects.get(content = payload['content'])
        old_like = comment.likes
        usde_url = LIKE_COMMENT_URL+str(comment.id)+'/'
        res = self.client.get(usde_url)
        comment = models.Comment.objects.get(content = payload['content'])
        new_like = comment.likes
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(old_like+1, new_like)
        matching_users = [user for user in comment.liked_users.all() if user.email == self.user.email]
        self.assertIn(self.user, matching_users)

        