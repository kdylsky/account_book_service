from django.db import models
from accountbook_service.models import BaseModel
from user.models import User


class Calendar(BaseModel):
    date = models.DateField(null= False)
    month_total = models.IntegerField(null = False, default = 0)


class AccountBook(BaseModel):
    calendar = models.OneToOneField(
        Calendar, 
        on_delete=models.CASCADE,
        db_column="calendar_id")
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        db_column="user_id"
    )
    day_total = models.IntegerField(null = False, default = 0)
    status = models.CharField(max_length=1, default="E")

    class Meta:
        db_table= "accountbooks"
        abstract = False
        managed = True


class Money(BaseModel):
    class MoneyTpye(models.TextChoices):
        INCOME = "income"
        PAY = "pay"

    accountbook = models.ForeignKey(
        AccountBook,
        on_delete = models.CASCADE,
        db_column = "accountbook_id"
    )
    money_type  = models.CharField(max_length=6, choices=MoneyTpye.choices, null = False)
    detail_type = models.CharField(max_length=1, default= "E", null= False)
    money = models.IntegerField(null = False)
    memo = models.TextField(null= True)
    status = models.CharField(max_length=1, default="E", null = False)

    class Meta:
        db_table = "money"
        abstract = False
        managed = True 