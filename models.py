import datetime
import uuid

from peewee import (
    SqliteDatabase, Model, CharField, TextField, DecimalField,
    IntegerField, ForeignKeyField, DateTimeField, BooleanField, DateField, UUIDField
)

db = SqliteDatabase("betsy.db")


class BaseModel(Model):
    class Meta:
        database = db


class TagError(Exception):
    pass

class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    username = CharField(unique=True, index=True)
    name = CharField()
    address = CharField()
    zipcode = CharField()
    city = CharField()
    state = CharField()
    country = CharField()
    billing_name = CharField()
    billing_account = CharField()
    password = CharField()
    email = CharField()
    updated_at = DateTimeField(null=True)
    created_by = ForeignKeyField('self', null=True, backref='users')


class Product(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, index=True)
    description = TextField()
    price_per_unit = DecimalField()
    quantity_in_stock = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)


class Tag(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, index=True)
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)
    color = CharField(null=True)
    parent = ForeignKeyField('self', null=True, backref='children')

    class Meta:
        database = db


class ProductTag(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, index=True)
    description = TextField(null=True)
    tag = ForeignKeyField(Tag, backref='related_products')
    product = ForeignKeyField(Product, backref='associated_tags')
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)

    class Meta:
        database = db


class Purchase(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKeyField(User, backref='user_purchases', on_delete='CASCADE')
    product = ForeignKeyField(Product, backref='product_purchases', on_delete='CASCADE')
    quantity = IntegerField()
    amount = DecimalField(max_digits=10, decimal_places=2)
    date = DateField(default=datetime.datetime.today)
    description = CharField(null=True)
    category = CharField(null=True)
    account = CharField(null=True)

    class Meta:
        database = db
    

class UserProduct(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKeyField(User, backref='user_products')
    product = ForeignKeyField(Product, backref='user_products')
    quantity = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)
    description = TextField(null=True)

    class Meta:
        database = db


