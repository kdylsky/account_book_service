from django.db import models

from accountbook_service.models import BaseModel

class User(BaseModel):
    name        = models.CharField(max_length=20, null=False)
    email       = models.CharField(max_length=100, null=False, unique = True)
    password    = models.CharField(max_length=255, null=False)
    plan_money  = models.IntegerField(null = False)

    class Meta:
        db_table = "users"
        abstract = False
        managed = True 