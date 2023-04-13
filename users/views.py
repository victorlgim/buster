from rest_framework.views import APIView, Request, Response, status
from .serializers import (UserSerializer, CustomJWTSerializer, UserProfile, UserSpecificSerializer,)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

class LoginView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer

class UserView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class UserSpecificView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, user_id):
        serializer = UserSpecificSerializer(data=request.data, context={"request": request, "user_id": user_id})
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserProfile(user, data=request.data, context={"request": request, "user_id": user_id})
        if serializer.is_valid():
            user = serializer.update(User.objects.get(pk=user_id), serializer.validated_data)
            return Response(UserSpecificSerializer(user).data, status=200)
        return Response(serializer.errors, status=403)
