from rest_framework import serializers
from user.models import User

class SignUpSchema(serializers.ModelSerializer):
    """
    회원가입을 위한 파라미터
    """
    class Meta:
        model = User
        fields = "__all__"


class LoginSchema(serializers.Serializer):
    """
    로그인을 위한 파라미터
    """
    email = serializers.CharField(max_length=100, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)
