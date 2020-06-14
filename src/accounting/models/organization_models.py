"""
Created at 13/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base_model import BaseClass
from ..constants import CONST_ORGANIZATION_TYPE
from ..utils import upload_image_to

CONST_LENGTH_NAME = 30


class Organization(BaseClass):
    """
    Organization class

    """
    name = models.CharField(_('Name'), max_length=CONST_LENGTH_NAME, unique=True)
    logo = models.ImageField(null=True,
                             blank=True,
                             upload_to=upload_image_to,
                             help_text="Organization logo used for display"
                             )
    type = models.CharField(max_length=20, choices=CONST_ORGANIZATION_TYPE, blank=True)


class Store(BaseClass):
    """Store entity owned by a single Owner."""
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta(object):
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return str(self.organization.name)


class Branch(BaseClass):
    """Branch entity which comes under a single Store."""
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta(object):
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return str(self.organization.name)
