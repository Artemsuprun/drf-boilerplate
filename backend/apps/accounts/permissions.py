from rest_framework.permissions import BasePermission

from .models import Role


class HasMinimumRole(BasePermission):
    """Base class: allow authenticated users whose role is at least `min_role`.

    Roles are read from the database on every request (JWTAuthentication loads the user),
    so a demotion takes effect immediately rather than when the access token expires.
    """

    min_role: str = Role.ADMIN

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.has_min_role(self.min_role))


class IsManagerOrAbove(HasMinimumRole):
    min_role = Role.MANAGER


class IsAdminRole(HasMinimumRole):
    min_role = Role.ADMIN
