from tortoise import fields
from tortoise.models import Model

class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=False)

    class Meta:
        abstract = True  

class Member(BaseModel):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    phone_number = fields.CharField(max_length=20)
    address = fields.TextField()
