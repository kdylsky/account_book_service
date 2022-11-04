from django.db import models
from accountbook_service.models import BaseModel
from user.models import User


class AccountBook(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        db_column="user_id"
    )
    day = models.DateField()
    day_total = models.IntegerField(null=False, default=0)
    delete_status = models.BooleanField(default=False)

    class Meta:
        db_table= "accountbooks"
        abstract = False
        managed = True


class Pay(BaseModel):
    accountbook = models.ForeignKey(
        AccountBook,
        on_delete = models.CASCADE,
        db_column = "accountbook_id"
    )
    money = models.IntegerField(null=False)
    title = models.CharField(max_length=30, null=False)
    memo = models.TextField(null=True)
    delete_status = models.BooleanField(default=False)

    class Meta:
        db_table = "pays"
        abstract = False
        managed = True 