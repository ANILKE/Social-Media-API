from .permissions import OwnerPermission

from rest_framework import permissions


class SelfUserPermissionMixin():
    permission_classes = [permissions.IsAdminUser, 
                          OwnerPermission]