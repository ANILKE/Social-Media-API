"""
Tests for post API.
"""
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post

from posts.serializers import PostSerializer,PostDetailSerializer

Create_Post_URL = reverse('posts:create')

def create_post(user, **params):
    """create and return a sample post"""
    defaults = {
        'content': "I like Pizza",
    }
    defaults.update(params)
    post = Post.objects.create(owner = user, **defaults)
    return post
    


class PublicPostApiTests(TestCase):
    """Test the public features of the post API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_post_not_allowed_for_unauth_user(self):
        """Test creating a post with a unauthenticated user is unsuccessful."""
        user = get_user_model().objects.create(email="testuser@example.com", password = "test123")
        payload = {
            'owner': user,
            'content': 'I like Pizza.',
            'likes': '3',
        }
        res = self.client.post(Create_Post_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        post = Post.objects.filter(owner=payload['owner'])
        self.assertFalse(post.exists())



class PrivateUserApiTests(TestCase):
    """Test post API requests that require authentication."""

    def setUp(self):
        self.user = get_user_model().objects.create(email="testuser@example.com", password="test123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    def test_create_post_with_auth_user(self):
        """Test creating a post with a authenticated user is successful."""
        payload = {
            'owner': self.user,
            'content': 'I like Pizza.',
            'likes': '3',
        }
        res = self.client.post(Create_Post_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(owner=payload['owner'])
        self.assertEqual(str(post),payload['content'])