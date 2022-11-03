from functools import wraps
import jwt
from django.conf import settings
from user.models import User
from provider.auth_provider import auth_provider
from user.exceptions import NotFoundUserError
from exceptions import NotAuthorizedError, TokenExpiredError
from datetime import datetime


def login_decorator():
    def decorator(api_func):
        @wraps(api_func)
        def wrapper(request, *args, **kwargs):
            try:
                access_token = request.headers.get('Authorization', None)
                if access_token == None: 
                    raise NotAuthorizedError()
                
                payload = jwt.decode(access_token, auth_provider.key, algorithms=["HS256"])                
                
                if payload["exp"] <= datetime.now().timestamp():
                    raise TokenExpiredError
                
                user         = User.objects.get(id = payload['id'])
                request.user = user
                return api_func(request, *args, **kwargs)
            
            except User.DoesNotExist:
                raise NotFoundUserError()        
        return wrapper
    return decorator
