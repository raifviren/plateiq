"""
Created at 13/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base_model import BaseClass
from .organization_models import Branch

CONST_LENGTH_NAME = 30


class Item(BaseClass):
    """Item for a branch."""
    name = models.CharField(_('Name'), max_length=CONST_LENGTH_NAME)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    price = models.FloatField(max_length=99999.99)
