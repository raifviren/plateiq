"""
Created at 13/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounting.utils import upload_image_to
from .base_model import BaseClass
from .item_models import Item
from .organization_models import Branch
from .user_models import Vendor
from .user_models import get_super_user_id

CONST_LENGTH_NAME = 30


class Document(BaseClass):
    """An document uploaded on the system."""
    file = models.FileField(null=False,
                            blank=False,
                            upload_to=upload_image_to)
    is_digitized = models.BooleanField(default=False)
    meta_data = JSONField(null=True,blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False,
                                   default=get_super_user_id)


class Invoice(BaseClass):
    """An invoice registered on the system."""
    branch = models.ForeignKey(Branch, related_name="invoices", on_delete=models.CASCADE, null=False, blank=False)
    vendor = models.ForeignKey(Vendor, related_name="invoices", on_delete=models.CASCADE, null=False, blank=False)
    invoice_num = models.CharField(_('Invoice Number'), max_length=CONST_LENGTH_NAME, null=False,
                                   blank=False)
    date = models.DateField(blank=False, null=False)
    total_amount = models.FloatField(max_length=99999999.99, null=False, blank=False)
    document = models.OneToOneField(Document, on_delete=models.CASCADE)

    class Meta:
        """
        Meta class for TestPackageTestInstance
        """
        unique_together = ("invoice_num", "vendor")


class InvoiceLineItem(BaseClass):
    """An item present on single invoice."""
    invoice = models.ForeignKey(Invoice, related_name="items_rels", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="invoice_rels", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(max_length=99999.99, null=False, blank=False)

    class Meta:
        """
        Meta class for TestPackageTestInstance
        """
        unique_together = ("invoice", "item")
