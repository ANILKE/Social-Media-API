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
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Followship)
admin.site.register(models.Comment)
admin.site.register(models.Post)

