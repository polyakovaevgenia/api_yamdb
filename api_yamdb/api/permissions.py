from rest_framework import permissions


class RoleAdminrOrReadOnly(permissions.BasePermission):
    """Доступ на чтение всем. Полный доступ админу и суперпользователю."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
