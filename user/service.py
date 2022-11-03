from user.repository import SignUpRepo
from provider.auth_provider import auth_provider

class SignService:
    def __init__(self):
        self.signup_repo = SignUpRepo()
    
    def create(self, name, email, password, plan_money):
        password = auth_provider.hash(password)
        
        create_user =self.signup_repo.create(
            name = name,
            email = email,
            password = password,
            plan_money = plan_money
        )

        return create_user