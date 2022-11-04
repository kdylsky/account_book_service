from accountbook.serializers import AccountBookSerializer, PaySerializer
from accountbook.models import AccountBook

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
    