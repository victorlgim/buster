from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from users.models import User


class UserOrEmployeeJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):

        authenticated_user = super().authenticate(request)
        if authenticated_user is None:
            return None
        user, token = authenticated_user
        if not user.is_employee:
            raise PermissionDenied("Usuário não é um funcionário")
        return user, token
