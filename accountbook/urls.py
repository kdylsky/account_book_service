from django.urls import path
from accountbook.controller import AccountBookAPI

urlpatterns = [
    path("accountbook", AccountBookAPI.as_view()),
    path("accountbook/deleted", AccountBookAPI.as_view())
]