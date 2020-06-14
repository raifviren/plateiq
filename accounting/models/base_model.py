"""
Created at 13/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals, absolute_import

import uuid

from django.db import models
from django.utils import timezone


class BaseClass(models.Model):
    """ Base Class for all models
        id          ==> is chosen to be uuid field to ensure intra-model uniqueness
        is_deleted  ==> will used to mark an instance as deleted. We will
                        NEVER delete any instance from DB untill unless we have a
                        solid explanation for it
        created_at  ==> non-editable
        updated_at  ==> non-editable
    """
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,
                          name="id", help_text="Unique ID")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BaseClass, self).save(*args, **kwargs)

    class Meta(object):
        """ abstract=True because we do not want duplicate models """
        abstract = True
        ordering = ['-created_at']
