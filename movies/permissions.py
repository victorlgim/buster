from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied

class AdminJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):

        authenticated_user = super().authenticate(request)
        if authenticated_user is None:
            return None
        user, token = authenticated_user
        if not user.is_employee:
            raise PermissionDenied("Usuário não é um administrador")
        return user, token
