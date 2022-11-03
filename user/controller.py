from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.views import APIView
from user.serializers import SignUpSchema
from user.service import SignService
from rest_framework import status

signup_service = SignService()

class SingUpAPI(APIView):
    def post(request):
        return signup(request)
    

@api_view(["POST"])
@parser_classes([JSONParser])
def signup(request):
    params = request.data
    params = SignUpSchema(data=params)
    params.is_valid(raise_exception=True)    

    created_user = signup_service.create(**params.data)

    return JsonResponse(created_user, status=status.HTTP_201_CREATED)


