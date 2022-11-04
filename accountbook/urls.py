from django.urls import path
from accountbook.controller import AccountBookAPI, DeleteAPI, PayObjectAPI,PayPartialUpdateView

urlpatterns = [
    path("accountbook", AccountBookAPI.as_view()),
    path("accountbook/<str:day>", PayObjectAPI.as_view()),
    path("accountbook/<str:day>/<int:id>", PayPartialUpdateView.as_view()),
    path("deleted", DeleteAPI.as_view()),
]