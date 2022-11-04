from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import login_decorator
from accountbook.serializers import AccountPostSchema
from accountbook.service import BookService

book_service = BookService()

class AccountBookAPI(APIView):
    def post(self, request):
        return post(request)
    
    def get(self, request):
        return get(request)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def post(request): # Todo:음수값이 들어오는 경우 예외처리 하기
    user = request.user
    params = request.data
    params = AccountPostSchema(data=params)
    params.is_valid(raise_exception=True)
    return JsonResponse(book_service.book_create(user, **params.data), status=status.HTTP_201_CREATED)


@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def get(request):
    return JsonResponse(book_service.get_list(request), status=status.HTTP_200_OK, safe=False) 