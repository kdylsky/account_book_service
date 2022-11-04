from datetime import datetime
from dateutil.relativedelta import relativedelta
from accountbook.models import AccountBook, Pay
from accountbook.serializers import AccountBookSerializer, PaySerializer, PayListSerializer

class BookRepo:
    def __init__(self)-> None:
        self.serializer_one = AccountBookSerializer
        self.serializer_two = PaySerializer
        self.model_one = AccountBook
    
    def create_book(self,user: object, day: str)-> object:
        serialize = self.serializer_one(
            data={
                "user":user.id,
                "day":day
            })
        serialize.is_valid(raise_exception=True)
        obj, flag = self.model_one.objects.get_or_create(user=user,day=day)        
        return obj
        
    def create_pay(self, accountbook:object, money: int, title: str, memo: str)-> dict:
        serialize = self.serializer_two(
            data={
                "accountbook":accountbook.id,
                "money":money,
                "title":title,
                "memo":memo
            })
        serialize.is_valid(raise_exception=True)
        serialize.save()
        accountbook.day_total += money
        accountbook.save()
        return serialize.data
    
    def get_list(self, request)-> list:
        user=request.user
        offset=request.GET.get("offset", 1)
        before_one_month = datetime.now() - relativedelta(months=int(offset))
        account = self.model_one.objects.filter(user=user, day__gte=before_one_month, delete_status=False).order_by("-day")
        account = self.serializer_one(instance=account, many=True)
        return account.data

    def delete_book(self,request)-> bool:
        user=request.user
        delete_list= request.GET.getlist("delete_list")
        objs = self.model_one.objects.filter(id__in=delete_list,user=user)
        objs.update(delete_status=True)
        cnt=[obj.pay_set.update(delete_status=True) for obj in objs]
        
        if cnt:
            return True # 삭제 성공
        else:
            return False # 삭제 실패
    
    def deletd_booklist(self, request)-> dict:
        user=request.user
        deleted_account = self.model_one.objects.filter(user=user,delete_status=True).order_by("-day")
        deleted_account = self.serializer_one(instance=deleted_account, many=True)
        return deleted_account.data
     
    def recovey_booklist(self, request)-> bool:
        user = request.user
        recovery_list= request.GET.getlist("recovery_list")
        objs = self.model_one.objects.filter(id__in=recovery_list,user=user)
        objs.update(delete_status=False)
        [obj.pay_set.update(delete_status=False) for obj in objs]

        if objs:
            return True #복구 성공
        else:
            return False #복구 실패


class PayRepo:
    def __init__(self):
        self.model_pay = Pay
        self.model_book = AccountBook
        self.serialize_one = PayListSerializer
        self.serialize_two = AccountBookSerializer
    
    def get_list_pay(self, request, day: str)-> list:
        user = request.user
        pay_obj = self.model_pay.objects.filter(accountbook__day=day,accountbook__user=user)
        serialize = self.serialize_one(instance=pay_obj, many=True)
        return serialize.data

    def delete_day_pay(self, request, day: str)-> bool:
        user = request.user
        delete_list = request.GET.getlist("delete_list", None)
        pay_objs = self.model_pay.objects.select_related("accountbook").filter(id__in=delete_list, accountbook__day=day, accountbook__user=user, delete_status=False)
 
        for pay_obj in pay_objs:
            pay_obj.delete_status = True
            pay_obj.accountbook.day_total -= pay_obj.money
            pay_obj.accountbook.save()
            pay_obj.save()

        if pay_objs:
            return True # 삭제성공
        else:
            return False # 삭제실패
    
    def patch_day_pay(self,request,day: str)-> bool:
        user = request.user
        recovy_list = request.GET.getlist("recovy_list", None)
        pay_objs = self.model_pay.objects.select_related("accountbook").filter(id__in=recovy_list, accountbook__day=day, accountbook__user=user, delete_status=True)

        for pay_obj in pay_objs:
            pay_obj.delete_status = False
            pay_obj.accountbook.day_total += pay_obj.money
            pay_obj.accountbook.save()
            pay_obj.save()

        if pay_objs:
            return True # 복구성공
        else:
            return False # 복구실패