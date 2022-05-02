
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.models import BaseModel


class Category(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True, null=True)
    description = models.CharField(max_length=1000, db_column='description', null=True, blank=True)
    deleted_flag = models.BooleanField(db_column='deleted_flag', default=False)

    class Meta(BaseModel.Meta):
        db_table = 'category'
        verbose_name_plural = _('Category')
