from rest_framework import permissions
from rest_framework.authtoken.models import Token


class IsNewUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = Token.objects.get(key=request.headers.get('token')).user
        except Token.DoesNotExist:
            return False
        if request.method == 'POST' or user:
            return True
        return False


class IsUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = Token.objects.get(key=request.headers.get('token')).user
        except Token.DoesNotExist:
            return False
        return user is not None

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            user = Token.objects.get(key=request.headers.get('token')).user
        except Token.DoesNotExist:
            return False
        return user == obj.user

