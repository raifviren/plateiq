"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import absolute_import

from django.conf.urls import url, include

from .base_urls import urlpatterns as base_urls

app_name = 'community'

urlpatterns = [
    url(r'^', include(base_urls)),
]
