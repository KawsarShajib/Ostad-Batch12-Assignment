from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Only the account owner or an admin can access the object."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == request.user