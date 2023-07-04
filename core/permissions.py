from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'You are not owner'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        if request.user.is_staff or request.user.is_superuser:
            return True