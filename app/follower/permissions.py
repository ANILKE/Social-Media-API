from rest_framework import permissions

class OwnerPermission(permissions.BasePermission):
    """Permissions for owners of object"""
    def has_object_permission(self, request, view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.following == request.user or obj.follower == request.user:
            return True
        return False

