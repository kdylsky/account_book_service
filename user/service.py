from user.repository import SignUpRepo
from provider.auth_provider import auth_provider
from user.models import User
from user.exceptions import CheckPasswordError

class SignService:
    def __init__(self):
        self.signup_repo = SignUpRepo()
    
    def create(self, name, email, password, plan_money):
        auth_provider.check_email(email)
        auth_provider.check_password(password)
        password = auth_provider.hashpw(password)
        create_user =self.signup_repo.create(
            name = name,
            email = email,
            password = password,
            plan_money = plan_money
        )

        return create_user


class LoginService:
    def login(self, email, password):
        user = User.objects.get(email=email)    
        if not auth_provider.check_password(password, user.password):
            raise CheckPasswordError()
        token = auth_provider.create_token(user.id)
        return token