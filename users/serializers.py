from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_employee"] = user.is_employee

        return token

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="username already taken.")],
    )
    email = serializers.CharField(
        max_length=127,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="email already registered.")]
    )
    password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField(required=False)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_is_employee(self, value):
        return value

    def create(self, validated_data):
        if validated_data["is_employee"] is True:
            return User.objects.create_superuser(**validated_data, is_superuser=True)
        return User.objects.create_user(**validated_data)


class UserSpecificSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_employee", "birthdate", "is_superuser"]
        read_only_fields = ("id", "username", "email", "first_name", "last_name", "is_employee", "birthdate", "is_superuser")

    def validate(self, _):
        request = self.context.get("request")
        user_id = self.context.get("user_id")
        user_infos = User.objects.get(pk=user_id)
        if not request.user.is_authenticated:
            raise AuthenticationFailed("Usuário não autenticado")

        if request.user.is_employee:
            return user_infos

        if user_id == request.user.id:
            return user_infos
        if not request.user.is_employee and user_id != request.user.id:
            raise PermissionDenied("Você não tem permissão para acessar este usuário")

        raise AuthenticationFailed("Você não tem permissão para acessar este usuário")


class UserSpecificEditSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="username already taken.")],
        required=False,
    )
    email = serializers.CharField(
        max_length=127,
        validators=[UniqueValidator(queryset=User.objects.all(), message="email already registered.")],
        required=False,
    )
    password = serializers.CharField(write_only=True, required=False)
    birthdate = serializers.DateField(required=False)
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email","first_name", "last_name","is_employee", "password", "birthdate", "is_superuser",]
        read_only_fields = ("id", "is_employee", "is_superuser")
        write_only_fields = "password"

    def validate(self, data):
        request = self.context.get("request")
        user_id = self.context.get("user_id")

        if not request.user.is_authenticated:
            raise AuthenticationFailed("Usuário não autenticado")

        if request.user.is_employee:
            return data

        if user_id == request.user.id:
            return data
        if not request.user.is_employee and user_id != request.user.id:
            raise PermissionDenied("Você não tem permissão para acessar este usuário")

        raise AuthenticationFailed("Você não tem permissão para acessar este usuário")

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.password = make_password(validated_data.get("password", instance.password))
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)

        instance.save()

        return instance
