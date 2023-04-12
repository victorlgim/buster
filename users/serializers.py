from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(User.objects.all(), message="email already registered.")
        ],
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(User.objects.all(), message="username already taken.")
        ]
    )
    birthdate = serializers.DateField(default=None)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        if validated_data["is_employee"]:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password')

        if password:
            instance.set_password(password)
            instance.save()        

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()        
        return instance