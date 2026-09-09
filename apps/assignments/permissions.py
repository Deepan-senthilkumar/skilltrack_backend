from rest_framework import permissions


class IsInstructor(permissions.BasePermission):
    """
    Allows read access to all and write access to authenticated instructors/admins.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(
            getattr(request.user, 'is_instructor', False) or
            getattr(request.user, 'is_staff', False) or
            getattr(request.user, 'is_superuser', False) or
            getattr(request.user, 'role', '') in ['ADMIN', 'STAFF']
        )

