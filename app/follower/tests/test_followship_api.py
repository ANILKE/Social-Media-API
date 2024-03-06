"""
Tests for friendships.
"""
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Followship

from follower.serializers import FriendshipSerializer,FriendshipDetailSerializer

FOLLOWERS_URL = reverse('user:followers:follower-list')

def create_friendship(user1, user2, **params):
    """create and return a sample friendship"""
    defaults = {
        'profile_link': "localhost:8000/api/user/1",
    }
    defaults.update(params)
    friendship = Followship.objects.create(following = user1, follower = user2, **defaults)
    return friendship
    


class PublicFriendshipAPITest(TestCase):
    """Test unauthenticated API requests"""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        """Test auth is required call API"""
        res = self.client.get(FOLLOWERS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

class PrivateFriendshipAPITest(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test1@example.com",
            "test123",
        )
        self.user2 = get_user_model().objects.create_user(
            "test2@example.com",
            "test123",
        )
        self.user3 = get_user_model().objects.create_user(
            "test3@example.com",
            "test123",
        )
        self.client.force_authenticate(self.user)
        # self.client.force_authenticate(self.user2)
        # self.client.force_authenticate(self.user3)

    def test_retrieve_friendships_limited_to_user(self):
        """Test friends list for specific user"""
        create_friendship(self.user,self.user2)
        create_friendship(self.user,self.user3)
        create_friendship(self.user2,self.user3)
        res = self.client.get(FOLLOWERS_URL)
        friendships = Followship.objects.filter(following = self.user)
        serializer = FriendshipDetailSerializer(friendships, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
