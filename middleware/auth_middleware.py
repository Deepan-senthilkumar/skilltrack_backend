from functools import wraps
from rest_framework import permissions, status
from rest_framework.response import Response
from utils.response import send_error


class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to Super Admins (ADMIN role or is_superuser).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN')


class IsAdminOrStaff(permissions.BasePermission):
    """
    Allows access to Admin or Staff / Instructors.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(
            request.user.is_superuser or
            getattr(request.user, 'role', '') in ['ADMIN', 'STAFF']
        )


class IsStudentUser(permissions.BasePermission):
    """
    Allows access to enrolled students.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


def require_roles(*allowed_roles):
    """
    Decorator for APIView methods requiring specific roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return send_error("Authentication required.", status_code=status.HTTP_401_UNAUTHORIZED)
            
            user_role = getattr(request.user, 'role', 'STUDENT')
            if request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)

            if user_role not in allowed_roles:
                return send_error(
                    f"Access denied. Requires one of: {list(allowed_roles)}",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
