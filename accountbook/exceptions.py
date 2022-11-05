from rest_framework import status
from exceptions import CustomBaseExecption

class ZeroMoneyError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Money Can not be Negative Integer"
        self.status = status.HTTP_400_BAD_REQUEST


class NotFoundCheckDeleteParams(CustomBaseExecption):
    def __init__(self):
        self.msg = "Not Found check delete_list params"
        self.status = status.HTTP_400_BAD_REQUEST


class NotFoundCheckRecoveryParams(CustomBaseExecption):
    def __init__(self):
        self.msg = "Not Found check recovery_list params"
        self.status = status.HTTP_400_BAD_REQUEST

