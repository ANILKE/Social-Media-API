"""
Django Admin Costumization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email' ,'name']
    fieldsets = (
        (None,{'fields': ('email', 'password','name',)}),
        (_('Permissions'),{'fields': ('is_active', 'is_superuser','is_staff',)}),
        (_('Important Dates'),{'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #Page look
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
            }),
    )
class FollowerAdmin(admin.ModelAdmin):
    """Define the admin pages for followship."""
    ordering = ['id']
    list_display = ['id','following' ,'follower']
    fieldsets = (
        (None,{'fields': ('following','follower',)}),
        (_('Follower User Profile'),{'fields': ('profile_link',)}),
        (_('Important Dates'),{'fields': ('since',)}),
    )
    readonly_fields = ['since']
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #Page look
            'fields': (
                'follower',
                'following',
                'since',
                'profile_link',
            ),
            }),
    )
class PostsAdmin(admin.ModelAdmin):
    """Define the admin pages for posts."""
    ordering = ['id']
    list_display = ['id','owner']
    fieldsets = (
        (None,{'fields': ('owner',)}),
        (_('Post Content'),{'fields': ('content',)}),
        (_('Post Interactions'),{'fields': ('comments','likes','liked_users')}),
    )
    readonly_fields = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #Page look
            'fields': (
                'owner',
                'content',
                'like',
                'liked_users',
            ),
            }),
    )
class CommentsAdmin(admin.ModelAdmin):
    """Define the admin pages for comments."""
    ordering = ['id']
    list_display = ['id','owner','related_post_id']
    fieldsets = (
        (None,{'fields': ('owner',)}),
        (_('Comment Content'),{'fields': ('content',)}),
        (_('Comment Interactions'),{'fields': ('likes','liked_users')}),
        (_('Related Post'),{'fields': ('related_post_id',)}),
    )
    readonly_fields = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #Page look
            'fields': (
                'owner',
                'content',
                'like',
                'liked_users',
                'related_post_id',
            ),
            }),
    )
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Followship,FollowerAdmin)
admin.site.register(models.Comment,CommentsAdmin)
admin.site.register(models.Post,PostsAdmin)

