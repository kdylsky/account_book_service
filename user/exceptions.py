from rest_framework import status
from exceptions import CustomBaseExecption


class CheckPasswordError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Please check your E-mail or Password"
        self.status = status.HTTP_400_BAD_REQUEST


class FormatPasswordError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Please check your Password Format"
        self.status = status.HTTP_400_BAD_REQUEST


class FormatEmailError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Please check your Email Format"
        self.status = status.HTTP_400_BAD_REQUEST



