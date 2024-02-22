from django.db import models
import uuid
import datetime
from user.models import User
# Create your models here.


def uuid_generate():
    return uuid.uuid4().hex
# Create your models here


class MyCustomField(models.DateTimeField):
    def db_type(self, connection):
        return 'timestamp'


class BaseModel(models.Model):
    id = models.CharField(max_length=32, unique=True,
                          primary_key=True, default=uuid_generate)
    creaed_at = MyCustomField(null=True)
    created_by = models.ForeignKey(
        "user.User", on_delete=models.PROTECT, related_name="+", db_column="created_by")
    updated_at = MyCustomField(null=True)
    updated_by = models.CharField(max_length=150)
    is_void = models.BooleanField(default=False)
    void_remarks = models.CharField(max_length=150, null=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.ForeignKey(
        'clg_api.Category', null=True, on_delete=models.PROTECT, related_name="+")
    sub_category = models.ForeignKey(
        'clg_api.SubCategory', null=True, on_delete=models.PROTECT, related_name="+")
    manufactured_date = models.DateField(
        default=datetime.datetime.now(), null=True)
    photo = models.BinaryField(null=True)
    description = models.TextField(null=True)
    vendor_id = models.ForeignKey(
        User, on_delete=models.PROTECT, db_column='vendor_id', related_name='+', null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.id


class Order(BaseModel):
    customer = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name="+")
    product = models.ForeignKey(
        Product, null=True, on_delete=models.PROTECT, related_name="+")
    vendor_id = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="+", db_column='vendor_id', null=True)
    rating = models.IntegerField(null=True)
    comment = models.CharField(max_length=200, null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        db_table = "order"

    def __str__(self) -> str:
        return self.product.id


class Province(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'province'

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    province_id = models.ForeignKey(
        Province, on_delete=models.PROTECT, db_column='province_id', related_name="+")

    class Meta:
        db_table = 'district'

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=100)
    province_id = models.ForeignKey(
        Province, on_delete=models.PROTECT, db_column='province_id', related_name="+")
    district_id = models.ForeignKey(
        District, on_delete=models.PROTECT, db_column='district_id', related_name="+")

    class Meta:
        db_table = 'municipality'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category, related_name="+", on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'sub_category'

    def __str__(self):
        return self.name


class AddToCard(models.Model):
    customer_id = models.CharField(max_length=32, null=True)
    product_id = models.CharField(max_length=32, null=True)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'add_to_card'

    def __str__(self):
        return self.id
