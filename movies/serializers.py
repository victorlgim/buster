from rest_framework import serializers
from .models import Movie, Ratings, MovieOrder

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    synopsis = serializers.CharField(required=False)
    rating = serializers.ChoiceField(choices=Ratings, required=False, default=Ratings.G)
    duration = serializers.CharField(required=False)
    added_by = serializers.CharField(read_only=True)
    added_by = serializers.SerializerMethodField()

    def create(self, validated_data):
        self.context.get("request")
        movie = Movie.objects.create(**validated_data)
        return movie

    class Meta:
        model = Movie
        fields = ["id", "title", "duration", "rating", "synopsis", "added_by"]
        read_only_fields = ("id", "added_by")

    def get_added_by(self, obj):
        return obj.user.email

class MovieDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.ReadOnlyField(source="movie.title")
    buyed_by = serializers.ReadOnlyField(source="user.email")
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, coerce_to_string=True)

    class Meta:
        model = MovieOrder
        fields = ["id", "title", "price", "buyed_by", "buyed_at"]
        read_only_fields = ["id", "title", "buyed_by", "buyed_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        movie_id = self.context.get("movie_id")
        movie = Movie.objects.get(id=movie_id)
        order = MovieOrder.objects.create(movie=movie, user=user, **validated_data)
        return order

    def get_buyed_by(self, obj):
        return obj.user.email

    def get_movie(self, obj):
        return obj.movie.title
