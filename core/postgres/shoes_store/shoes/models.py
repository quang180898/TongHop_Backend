import base64
import io
from PIL import Image
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.models import BaseModel
from core.postgres.shoes_store.category.models import Category
from library.constant.api import GENDER_TYPE_CHOICE, GENDER_TYPE_MALE


class Brand(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True, null=True)
    code = models.IntegerField(db_column='permission_code', null=True, blank=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'brand'
        verbose_name_plural = _('Brand')


class Shoes(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    brand = models.ForeignKey(
        Brand, db_column='brand_id',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('BrandID')
    )
    name = models.CharField(max_length=150, db_column='name', blank=True, null=True)
    code = models.IntegerField(db_column='shoes_code', null=True, blank=True)
    gender = models.IntegerField(
        db_column='gender',
        default=GENDER_TYPE_MALE,
        blank=True, null=True,
        choices=GENDER_TYPE_CHOICE
    )
    retail_price = models.IntegerField(db_column='retail_price', null=True, blank=True)
    wholesale_price = models.IntegerField(db_column='wholesale_price', null=True, blank=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'shoes'
        verbose_name_plural = _('Shoes')


class Shoes_quantity(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    shoes = models.ForeignKey(
        Shoes, db_column='shoes_id',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('ShoesID')
    )
    size = models.IntegerField(db_column='size', null=True, blank=True)
    quantity = models.IntegerField(db_column='quantity', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'shoes_quantity'
        verbose_name_plural = _('Shoes Quantity')


class Shoes_discount(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    shoes = models.ForeignKey(
        Shoes, db_column='shoes_id',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('ShoesID')
    )
    discount_percent = models.IntegerField(db_column='discount_percent', null=True, blank=True)
    end_discount_date = models.DateTimeField(db_column='end_discount_date', blank=True, null=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'shoes_discount'
        verbose_name_plural = _('Shoes Discount')


class Shoes_category(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    shoes = models.ForeignKey(
        Shoes, db_column='shoes_id',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('ShoesID')
    )
    category = models.ForeignKey(
        Category, db_column='category_id',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('CategoryID')
    )
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'shoes_category'
        verbose_name_plural = _('Shoes Category')


class Shoes_image(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    shoes = models.ForeignKey(
        Shoes, db_column='shoes_id',
        blank=True, null=True,
        on_delete=models.PROTECT,
        verbose_name=_('ShoesID')
    )
    image_bytes = models.BinaryField(db_column='image_bytes')
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)
    class Meta(BaseModel.Meta):
        db_table = 'shoes_image'
        verbose_name_plural = _('Shoes Image')

    @property
    def get_image(self):
        try:
            return base64.b64encode(self.image_bytes).decode('utf-8')
        except:
            return None
