import base64
import io
from PIL import Image
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.shoes_store.permission.models import Permission
from core.postgres.shoes_store.category.models import Category
from core.postgres.shoes_store.shoes.models import Shoes
from core.postgres.models import BaseModel
from library.constant.api import GENDER_TYPE_MALE, GENDER_TYPE_CHOICE


class Customer(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True)
    username = models.CharField(max_length=50, db_column='username', blank=True)
    password = models.CharField(max_length=255, db_column='password', null=True, blank=True)
    mail = models.CharField(max_length=255, db_column='mail', null=True, blank=True)
    mobile = models.CharField(max_length=10, db_column='mobile', blank=True, null=True)
    address = models.CharField(max_length=255, db_column='address', null=True, blank=True)
    permission = models.ForeignKey(
        Permission, db_column='permission_id',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Permission')
    )
    gender = models.IntegerField(
        db_column='gender',
        default=GENDER_TYPE_MALE,
        blank=True, null=True,
        choices=GENDER_TYPE_CHOICE
    )
    birthdate = models.DateTimeField(db_column='birthdate', null=True, blank=True)
    image_bytes = models.BinaryField(db_column='image_bytes')
    active_flag =  models.BooleanField(db_column='active_flag', default=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'customer'
        verbose_name_plural = _('Customer')

    @property
    def get_image(self):
        try:
            return base64.b64encode(self.image_bytes).decode('utf-8')
        except:
            return None

    @property
    def get_thumbnail(self):
        try:
            image = Image.open(io.BytesIO(self.image_bytes))
            image.thumbnail((90, 90))
            data = io.BytesIO()
            image.save(data, format="PNG")
            return base64.b64encode(data.getvalue()).decode('utf-8')
        except:
            return None


class Customer_shoes(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    Customer = models.ForeignKey(
        Customer, db_column='customer',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Customer')
    )
    shoes = models.ForeignKey(
        Shoes, db_column='shoes',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Shoes')
    )
    quantity = models.IntegerField(db_column='quantity', null=True, blank=True)
    size = models.IntegerField(db_column='size', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'customer_shoes'
        verbose_name_plural = _('Customer Shoes')


class Customer_favorite(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    Customer = models.ForeignKey(
        Customer, db_column='customer',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Customer')
    )
    category = models.ForeignKey(
        Category, db_column='category',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Category')
    )
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'customer_favorite'
        verbose_name_plural = _('Customer Favorite')


class Customer_debt(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    Customer = models.ForeignKey(
        Customer, db_column='customer',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Customer')
    )
    prepay = models.IntegerField(db_column="prepay", null=True, blank=True) # trả trước
    debt = models.IntegerField(db_column="debt", null=True, blank=True) # dư nợ còn lại
    status = models.CharField(max_length=20, db_column='status', default='Chưa Thanh Toán')
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'customer_debt'
        verbose_name_plural = _('Customer Debt')