from rest_framework import permissions


class IsInstructor(permissions.BasePermission):
    """
    Allows access only to staff/instructors.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_instructor)
