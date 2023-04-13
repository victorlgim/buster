from django.shortcuts import render
from rest_framework.views import APIView, Response
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Movie
from .permissions import AdminJWTAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = MovieSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        movies = Movie.objects.all().order_by('id')
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class MovieSpecificView(APIView):
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, _, movie_id):
        try:
            Movie.objects.get(pk=movie_id).delete()
        except Movie.DoesNotExist:
            return Response(status=404)
        return Response(status=204)

    def get(self, _, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=200)
        except Movie.DoesNotExist:
            return Response(status=404)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, movie_id):
        serializer = MovieOrderSerializer(
            data=request.data, context={"request": request, "movie_id": movie_id}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
