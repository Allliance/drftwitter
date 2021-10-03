from rest_framework import permissions


class IsNewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method