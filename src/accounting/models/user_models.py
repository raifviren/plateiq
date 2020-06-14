"""
Created at 13/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from .base_model import BaseClass
from .organization_models import Organization
from ..constants import CONST_USER_TYPE
from ..utils import upload_image_to

# Create your models here.

# Constants
USER_PHONE_MAX_LEN = 15


class User(BaseClass, AbstractUser):
    """
    User class

    No new members are needed beyond the standard fields provided by
    Django's AbstractUser class. However; a derivation is kept in to
    allow easy extension when needed without changing the table name
    (when using Django's AbstractUser the table would be auth_user,
    and when we have our own it would be core_user), which can effect
    other authentication related components like python social auth
    and authentication workflows e.g. OAuth2, login etc.

    """
    mobile = models.CharField(_('mobile number'),
                              max_length=USER_PHONE_MAX_LEN,
                              help_text=_('Enter mobile number'),
                              unique=True,
                              db_index=True
                              )
    country_code = models.CharField(_('country code'),
                                    max_length=5,
                                    help_text=_('Enter country code'),
                                    default='+91'
                                    )
    is_verified = models.BooleanField(default=False)
    photo = models.ImageField(null=True,
                              blank=True,
                              upload_to=upload_image_to,
                              help_text="User profile image used for display"
                              )
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=20, choices=CONST_USER_TYPE, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    @cached_property
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if not self.first_name and not self.last_name:
            return ""
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    get_full_name.short_description = "Name"

    @classmethod
    def get_user_by_mobile(cls, mobile):
        try:
            user = cls.objects.get(mobile=mobile)
            return user
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_user_by_email(cls, email):
        try:
            user = cls.objects.get(email=email)
            return user
        except ObjectDoesNotExist:
            return None

    def save(self, *args, **kwargs):
        """ On save, update username """
        if not self.username:
            self.username = self.mobile
        super(User, self).save(*args, **kwargs)


class Owner(BaseClass):
    """model for Purchaser/Buyer"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta(object):
        verbose_name = 'Merchant'
        verbose_name_plural = 'Merchants'

    def __str__(self):
        return str(self.user.first_name)


class Vendor(BaseClass):
    """model for Vendor/Seller"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.first_name)
