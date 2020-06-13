from __future__ import unicode_literals, absolute_import

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .constants import CONST_USER_TYPE
from .utils import upload_image_to

# Create your models here.


class BaseClass(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, name="id")
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    @classmethod
    def get_obj(cls, primary_key):
        """
        Get object by primary_key and return this object

        Params: cls, class object
                 primary_key
        Return: models object
        """
        try:
            return cls.objects.get(id=primary_key)
        except (cls.DoesNotExist, ValueError):
            return None
        except Exception:
            return None

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        self.updated_at = timezone.now()
        return super(BaseClass, self).save(*args, **kwargs)

    class Meta(object):
        abstract = True


class User(AbstractUser, BaseClass):
    mobile = models.CharField(_('mobile number'),
                              max_length=15,
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
                              )
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=20, choices=CONST_USER_TYPE, blank=True)

    @classmethod
    def get_user_by_mobile(cls, mobile):
        try:
            user = cls.objects.get(mobile=mobile)
            return user
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.mobile

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.mobile
        super(User, self).save(*args, **kwargs)