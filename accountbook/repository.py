from accountbook.serializers import AccountBookSerializer, PaySerializer
from accountbook.models import AccountBook
from datetime import datetime
from dateutil.relativedelta import relativedelta


class BookRepo:
    def __init__(self):
        self.serializer_one = AccountBookSerializer
        self.serializer_two = PaySerializer
        self.model_one = AccountBook
    
    def create_book(self,user: object, day: str)-> object:
        serialize = self.serializer_one(
            data={
                "user":user.id,
                "day":day
            }
        )
        serialize.is_valid(raise_exception=True)
        obj, flag = self.model_one.objects.get_or_create(user=user,day=day)        
        return obj
        
    def create_pay(self, accountbook:object, money: int, title: str, memo: str)->dict:
        serialize = self.serializer_two(
            data={
                "accountbook":accountbook.id,
                "money":money,
                "title":title,
                "memo":memo
            }
        )
        serialize.is_valid(raise_exception=True)
        serialize.save()
        accountbook.day_total += money
        accountbook.save()
        return serialize.data
    
    
    def get_list(self, request)-> list:
        user = request.user
        offset = request.GET.get("offset", 1)
        before_one_month = datetime.now() - relativedelta(months=int(offset))
        account = self.model_one.objects.filter(user=user, day__gte=before_one_month).order_by("-day")
        account = self.serializer_one(instance=account, many=True)
        return account.data
