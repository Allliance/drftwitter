import jwt.exceptions
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .serializers import decode_jwt


def validate_user_token(request):
    try:
        return Token.objects.get(key=request.headers.get('token')).user is not None
    except Token.DoesNotExist:
        return False


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return validate_user_token(request)


class TwitPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        try:
            user_permissions = decode_jwt(request.headers.get('jwt'))
        except jwt.exceptions.DecodeError:
            return False
        if request.method == 'POST':
            return user_permissions.get('post_twit')
        if request.method == 'PUT':
            return user_permissions.get('edit_twit')
        if request.method == 'DELETE':
            return user_permissions.get('delete_twit')
        return True


class UserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'POST']:
            return True
        try:
            user_permissions = decode_jwt(request.headers.get('jwt'))
        except jwt.exceptions.DecodeError:
            return False
        if request.method == 'PUT':
            return user_permissions.get('change_name')
        if request.method == 'DELETE':
            return user_permissions.get('delete_user')
        return True


class CommentPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            try:
                user_permissions = decode_jwt(request.headers.get('jwt'))
            except jwt.exceptions.DecodeError:
                return False
            return user_permissions.get('post_comment') is True and validate_user_token(request)
        return True
