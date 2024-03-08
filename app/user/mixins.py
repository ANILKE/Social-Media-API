from .permissions import selfUserPermission

from rest_framework import permissions


class SelfUserPermissionMixin():
    permission_classes = [permissions.IsAdminUser, 
                          selfUserPermission]

# class UserQuerySetMixin():
#     user_field= 'email'
#     def get_queryset(self, *args, **kwargs):
#         lookup_data = {}
#         lookup_data[self.user_field] = self.request.user.email
#         print(lookup_data[self.user_field])
#         qs = super().get_queryset(*args,**kwargs)
#         return qs.filter(**lookup_data)