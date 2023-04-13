from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:user_id>/", views.UserSpecificView.as_view()),
    path("users/login/", views.LoginView.as_view()),
    path("users/login/refresh/", jwt_views.TokenRefreshView.as_view()),
]
