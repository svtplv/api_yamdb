from rest_framework.permissions import (
    BasePermission,
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS
)


class IsAuthorStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return any((
            request.method in SAFE_METHODS,
            obj.author == self.request.user,
            request.user.is_mod,
            request.user.is_admin
        ))


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin
