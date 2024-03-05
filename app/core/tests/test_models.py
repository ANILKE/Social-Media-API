"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from .. import models
class ModelTests(TestCase):
    """Tests Models."""
    
    def test_create_user_with_email(self):
        """Test creating an user with email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "pass123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a new user without email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','pass123')

    def test_create_superuser(self):
        """Test creatin a superuser."""
        user = get_user_model().objects.create_superuser(
            'test123@example.com',
            'testpass123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_crete_followship(self):
        """Test creating a followship between 2 users."""
        user1 = get_user_model().objects.create_superuser(
            'test123@example.com',
            'testpass123',
        )
        user2 = get_user_model().objects.create_superuser(
            'test1234@example.com',
            'testpass1234',
        )
        followship = models.Followship.objects.create(
            following = user1,
            follower = user2,
            profile_link = "aaa.aaa",
        )
        self.assertEqual(str(followship),"aaa.aaa")

    def test_crete_post_without_comment(self):
        """Test creating a post by a user."""
        user1 = get_user_model().objects.create_superuser(
            'test123@example.com',
            'testpass123',
        )
        post = models.Post.objects.create(
            owner = user1,
            content = "I like pizza.",
        )
        self.assertEqual(str(post),"I like pizza.")
    def test_crete_post_without_comment1(self):
        """Test creating a post by a user."""
        user1 = get_user_model().objects.create_superuser(
            'test123@example.com',
            'testpass123',
        )
        comment1 = models.Comment.objects.create(
            owner = user1,
            content = "I like pizza too.",
            related_post_id = 1,
        )
        comment2 = models.Comment.objects.create(
            owner = user1,
            content = "I like pizza too too.",
            related_post_id = 1,
        )
        post = models.Post.objects.create(
            owner = user1,
            content = "I like pizza.",
        )
        post.comments.add(comment1)
        post.comments.add(comment2)
        self.assertEqual(str(post),"I like pizza.")
        # self.assertEqual(str(post.comments.all()),"I like pizza too.")
        # self.assertEqual(str(post.comments.all()),"I like pizza too too.")

        
    def test_crete_comment(self):
        """Test creatin a comment."""
        user1 = get_user_model().objects.create_superuser(
            'test123@example.com',
            'testpass123',
        )
        comment = models.Comment.objects.create(
            owner = user1,
            content = "I like pizza too.",
            related_post_id = 1,
        )
        self.assertEqual(str(comment),"I like pizza too.")