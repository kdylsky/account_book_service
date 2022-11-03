import bcrypt
import jwt
from django.conf import settings
from datetime import datetime


class AuthProvider:
    def __init__(self):
        self.key = settings.JWT_KEY
        self.expire_sec = settings.JWT_EXPIRE_TIME
    
    def hashpw(self, password: str):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def check_password(self, password: str, hash_pw: str):
        return bcrypt.checkpw(password.encode("utf8"), hash_pw.encode("utf8"))


    def create_token(self, user_id: str, is_expired: bool = False):
        exp = 0 if is_expired else self.get_curr_sec() + self.expire_sec
        encoded_jwt = jwt.encode(
            {"id": user_id, "exp": exp},
            self.key,
            algorithm="HS256",
        )
        return {"access": encoded_jwt}

    def get_curr_sec(self):
        return datetime.now().timestamp()

auth_provider = AuthProvider()