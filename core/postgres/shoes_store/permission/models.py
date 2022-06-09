from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.postgres.models import BaseModel


class Permission(BaseModel):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=150, db_column='name', blank=True, null=True)
    code = models.CharField(max_length=10, db_column='code', null=True, blank=True)

    class Meta(BaseModel.Meta):
        db_table = 'permission'
        verbose_name_plural = _('Permission')
