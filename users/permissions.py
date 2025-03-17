from rest_framework import permissions


class IsOwnerOrModer(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта или модератором."""

    def has_object_permission(self, request, view, obj):
        """Возвращает True, если пользователь является владельцем или модератором."""
        return (
            obj.owner == request.user
            or request.user.groups.filter(name="Модератор").exists()
        )
