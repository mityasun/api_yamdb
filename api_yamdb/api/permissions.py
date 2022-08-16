from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка, что админ или суперюзер и безопасный метод"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Проверка авторизации и доступа к объектам"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
    """Проверка, что админ или суперюзер"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
