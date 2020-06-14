"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from accounting.models import Document, Invoice
from accounting.serializers import DocumentSerializer, InvoiceSerializer
from .base_views import BaseViewSet


class DocumentViewSet(BaseViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


class InvoiceViewSet(BaseViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

