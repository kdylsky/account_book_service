from rest_framework import serializers
from accountbook.models import AccountBook, Pay


class AccountPostSchema(serializers.Serializer):
    """
    가계부 생성을 위한 요청 파라미터 스키마
    """
    day = serializers.DateField(allow_null=False)
    money = serializers.IntegerField(allow_null=False)
    title = serializers.CharField(max_length=30, allow_null=False)
    memo = serializers.CharField(max_length=None, allow_null=True)


class AccountBookSerializer(serializers.ModelSerializer):
    """
    AccountBook객체를 생성하는 serializer
    """
    class Meta:
        model = AccountBook
        fields = "__all__"
    

class PaySerializer(serializers.ModelSerializer):
    """
    Pay객체를 생성하는 serializer
    """
    class Meta:
        model = Pay
        fields = "__all__"
    