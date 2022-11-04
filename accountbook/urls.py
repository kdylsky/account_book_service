from django.urls import path
from accountbook.controller import AccountBookAPI, DeleteAPI

urlpatterns = [
    path("accountbook", AccountBookAPI.as_view()),
    path("deleted", DeleteAPI.as_view())
]