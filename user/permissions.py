from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "admin"
        )


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "doctor"
        )


class IsLabRole(BasePermission):   # ✅ THIS WAS MISSING
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "lab"
        )
