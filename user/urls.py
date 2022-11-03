from django.urls import path
from user.controller import SingUpAPI, LoginAPI, TestAPI

urlpatterns = [
    path("signup", SingUpAPI.as_view()),
    path("login", LoginAPI.as_view()),
]