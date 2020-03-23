""" Permissos de Usuario """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsUserAccount(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj