from rest_framework import status
from exceptions import CustomBaseExecption


class CheckPasswordError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Please check your E-mail or Password"
        self.status = status.HTTP_400_BAD_REQUEST





