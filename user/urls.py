from django.urls import path
from user.controller import SingUpAPI

urlpatterns = [
    path("/signup", SingUpAPI.as_view())
]