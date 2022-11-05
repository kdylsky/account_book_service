from user.models import User
from user.serializers import SignUpSchema

class SignUpRepo():
    def __init__(self):
        self.model = User
        self.serializer =SignUpSchema

    def create(self, name, email, password, plan_money):
        serializer = self.serializer(
            data={
                "name":name,
                "email":email,
                "password":password,
                "plan_money":plan_money
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
