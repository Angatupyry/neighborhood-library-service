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


class Book(BaseModel):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13, unique=True)
    available = fields.BooleanField(default=True)


class Borrow(BaseModel):
    id = fields.IntField(pk=True)
    member = fields.ForeignKeyField("models.Member", related_name="borrows")
    book = fields.ForeignKeyField("models.Book", related_name="borrows")
    borrow_date = fields.DatetimeField(auto_now_add=True)
    return_date = fields.DatetimeField(null=True)
