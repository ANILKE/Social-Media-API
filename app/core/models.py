"""
Models for Database.
"""

from typing import Any, Iterable, Sequence
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

from rest_framework.reverse import reverse


class UserManager(BaseUserManager):
    """Manager for system users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User need to have an email address!')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'

class FollowshipManager(models.Manager):
    def create(self, **kwargs):
        # qs =Followship.objects.filter(following = kwargs['following']).filter(follower = kwargs['follower'])
        # if(qs.exists()):
        #     raise("Already friends")
        # return super.create(**kwargs)

        pass
    
class Followship(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'follower')
    since = models.DateTimeField(default = timezone.now)
    profile_link = models.CharField(max_length =255,blank = True)
    objects = FollowshipManager
    def __str__(self):
        return self.profile_link
    
class Comment(models.Model):
    #content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE, related_name = 'type')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'comment_owner')
    content = models.CharField(max_length =255,blank = True)
    likes = models.IntegerField(default = 0)
    liked_users = models.ManyToManyField(User, blank= True)
    related_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name = 'related_post')
    create_time = models.DateTimeField(default = timezone.now)
    
    
    def __str__(self):
        return self.content
    
class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'post_owner')
    content = models.CharField(max_length =255,blank = True)
    likes = models.IntegerField(default = 0)
    comments = models.ManyToManyField(Comment, blank= True)
    liked_users = models.ManyToManyField(User, blank= True)
    create_time = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return self.content
