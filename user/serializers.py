from rest_framework import serializers
from user.models import User

class SignUpSchema(serializers.Serializer):
    """
    회원가입을 위한 파라미터 인자
    """
    class Meta:
        model = User
        fields = "__all__"
