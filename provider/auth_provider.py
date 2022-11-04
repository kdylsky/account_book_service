import bcrypt
import jwt
import re
from django.conf import settings
from datetime import datetime
from user.exceptions import FormatEmailError, FormatPasswordError

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


    def check_password_format(self, password):
        REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        if not re.match(REGEX_PASSWORD, password):
            raise FormatPasswordError()


    def check_email(self, email):
        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(REGEX_EMAIL, email):
            raise FormatEmailError()

auth_provider = AuthProvider()