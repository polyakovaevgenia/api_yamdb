from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """"Доступ для администратора и суперпользователя """

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                )


class RoleAdminrOrReadOnly(permissions.BasePermission):
    """Доступ на чтение всем. Полный доступ админу и суперпользователю."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminIsModeratorIsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ на чтение всем. Полный доступ автору, суперюзеру,
    админу и модератору."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user or request.user.is_admin
                    or request.user.is_moderator))
