from rest_framework import permissions
from rest_framework.authtoken.models import Token


class IsNewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            user = Token.objects.get(key=request.headers.get('token'))
        except Token.DoesNotExist:
            return False
        if request.method == 'POST' or user:
            return True
        return False
