from rest_framework import serializers
from movies.models import Rating, Movie, OrderMovie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    synopsis = serializers.CharField(default=None)
    rating = serializers.ChoiceField(
        choices=Rating.choices, default=Rating.G
    )
    duration = serializers.CharField(max_length=10, default=None)
    added_by = serializers.EmailField(source="user.email", read_only=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class OrderMovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source="movie.title", read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.CharField(source="user.email", read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return OrderMovie.objects.create(**validated_data)
        