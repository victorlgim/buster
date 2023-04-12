from rest_framework import permissions

class IsMovieUser(permissions.BasePermission):
    def has_object_permission(self, request, _, movie):

        return movie.user == request.user

