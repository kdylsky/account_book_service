from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.views import APIView
from user.serializers import SignUpSchema, LoginSchema
from user.service import SignService, LoginService
from rest_framework import status
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import login_decorator

signup_service = SignService()
login_service = LoginService()


class SingUpAPI(APIView):
    def post(self,request):
        return signup(request)


class LoginAPI(APIView):
    def post(self, request):
        return user_login(request)


@execption_hanlder()
@parser_classes([JSONParser])
def signup(request):
    params = request.data
    params = SignUpSchema(data=params)
    params.is_valid(raise_exception=True)    
    created_user = signup_service.create(**params.data)
    return JsonResponse(created_user, status=status.HTTP_201_CREATED)


@execption_hanlder()
@parser_classes([JSONParser])
def user_login(request):
    params = request.data
    params = LoginSchema(data=params)
    params.is_valid(raise_exception=True)
    token = login_service.login(**params.data)
    return JsonResponse(token, status=status.HTTP_201_CREATED)
