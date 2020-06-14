"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import absolute_import

from django.urls import path, include

from .user_urls import urlpatterns as user_urls

# from .invoice_urls import urlpatterns as invoice_urls
# from .item_urls import urlpatterns as item_urls


urlpatterns = [
    path('', include(user_urls)),
    # path('invoice/', include(invoice_urls)),
    # path('item/', include(item_urls)),
]
