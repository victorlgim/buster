from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from movies.models import Movie
from movies.serializers import MovieSerializer, OrderMovieSerializer
from users.permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication = [JWTAuthentication]
    permission = [IsEmployee]

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request):
        movies = Movie.objects.all().order_by('id')
        result_page = self.paginate_queryset (movies, request)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class MovieDetailView(APIView):
    authentication = [JWTAuthentication]
    permission = [IsEmployee]

    def get(self, _, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, _, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderMovieView(APIView):
    authentication = [JWTAuthentication]
    permission = [IsAuthenticated]

    def post(self, request, movie_id):
        movie_obj = get_object_or_404(Movie, id=movie_id)

        serializer = OrderMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, movie=movie_obj)

        return Response(serializer.data, status.HTTP_201_CREATED)
