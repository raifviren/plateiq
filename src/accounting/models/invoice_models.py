"""
Created at 13/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base_model import BaseClass
from .item_models import Item
from .organization_models import Branch
from .user_models import Vendor
from ..utils import upload_image_to

CONST_LENGTH_NAME = 30


class Document(BaseClass):
    """An document uploaded on the system."""
    file = models.FileField(null=False,
                            blank=False,
                            upload_to=upload_image_to)
    is_digitized = models.BooleanField(default=False)
    meta_data = JSONField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Invoice(BaseClass):
    """An invoice registered on the system."""
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    invoice_num = models.CharField(_('Invoice Number'), max_length=CONST_LENGTH_NAME, unique=True)
    date = models.DateField(blank=False, null=False)
    total_amount = models.FloatField(max_length=99999999.99)
    document = models.ForeignKey(Document, null=True)


class InvoiceLineItem(BaseClass):
    """An item present on single invoice."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(max_length=3)
    price = models.FloatField(max_length=99999.99)
