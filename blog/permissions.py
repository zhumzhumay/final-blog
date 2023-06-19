# from rest_framework.permissions import BasePermission
# from .models import User

# '''SUPERADMIN, SELLER, COURIER, ASSEMBLER, BASIC'''


# class IsReader(BasePermission):

#     def has_permission(self, request, view):
#         return request.user.role == User.READER


# # class IsEditor(BasePermission):

# #     def has_permission(self, request, view):
# #         return request.user.role == User.EDITOR


# class IsSuperAdmin(BasePermission):

#     def has_permission(self, request, view):
#         return request.user.role == User.SUPERADMIN
