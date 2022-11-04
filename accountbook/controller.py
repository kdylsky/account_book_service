from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.decorators import parser_classes
from accountbook.serializers import AccountPostSchema,PaySerializer
from accountbook.models import Pay
from accountbook.service import BookService, PayService
from decorators.auth_handler import login_decorator
from decorators.execption_handler import execption_hanlder

book_service = BookService()
pay_service = PayService()

class AccountBookAPI(APIView):
    def post(self, request):
        return post(request)
    
    def get(self, request):
        return get(request)

    def delete(self, request):
        return delete(request)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def post(request): # Todo:음수값이 들어오는 경우 예외처리 하기
    # 127.0.0.1:8000/accountbook
    user = request.user
    params = request.data
    params = AccountPostSchema(data=params)
    params.is_valid(raise_exception=True)
    return JsonResponse(book_service.create_book(user, **params.data), status=status.HTTP_201_CREATED)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def get(request):
    # 127.0.0.1:8000/accountbook
    # 127.0.0.1:8000/accountbook?offset=2
    return JsonResponse(book_service.get_list(request), status=status.HTTP_200_OK, safe=False) 

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def delete(request):
    # 127.0.0.1:8000/accountbook?delete_list=4&delete_list=5
    return JsonResponse(book_service.delete_book(request), status=status.HTTP_200_OK, safe=False)


class DeleteAPI(APIView):
    def get(self, request):
        return deleted_get(request)

    def patch(self, request):
        return deleted_patch(request)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def deleted_get(request):
    #127.0.0.1:8000/deleted
    return JsonResponse(book_service.deleted_booklist(request), status=status.HTTP_200_OK, safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def deleted_patch(request):
    # 127.0.0.1:8000/accountbook?recovey_list=4&recovey_list=5
    return JsonResponse(book_service.recovey_booklist(request), status=status.HTTP_200_OK, safe=False)


class PayObjectAPI(APIView):
    def get(self,request,day):
        return get_day(request,day)

    def delete(self, request,day):
        return delete_day(request,day)

    def patch(self,request,day):
        return patch_day(request,day)
    
@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def get_day(request, day):
    # 127.0.0.1:8000/accountbook/2022-10-15
    return JsonResponse(pay_service.get_pay_day(request, day),status=status.HTTP_200_OK,safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def delete_day(request, day):
    # 127.0.0.1:8000/accountbook/2022-10-15?delete_list=6&delete_list=5
    return JsonResponse(pay_service.delete_pay_day(request,day), status=status.HTTP_200_OK, safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def patch_day(request, day):
    # 127.0.0.1:8000/accountbook/2022-10-15?delete_list=6
    return JsonResponse(pay_service.patch_pay_day(request,day), status = status.HTTP_200_OK, safe=False)


class PayPartialUpdateView(GenericAPIView, UpdateModelMixin):
    def put(self, request, *args, **kwargs):
        return partial_update(request, *args, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
@login_decorator()
def partial_update(request, *args, **kwargs):
    #127.0.0.1:8000/accountbook/2022-10-15/5
    kwargs['partial'] = True
    return update(request, *args, **kwargs)

def update(request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = Pay.objects.get(accountbook__user=request.user.id, accountbook__day= kwargs["day"], id = kwargs["id"])
    serializer = PaySerializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    perform_update(serializer)
    if getattr(instance, '_prefetched_objects_cache', None):
        instance._prefetched_objects_cache = {}
    return JsonResponse(serializer.data, status = status.HTTP_200_OK)

def perform_update(serializer):
    serializer.save()