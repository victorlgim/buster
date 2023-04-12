from rest_framework import permissions
from users.models import User


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, _):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_employee
        )

   
class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, _, obj):
        return request.user.is_employee or obj == request.user
        