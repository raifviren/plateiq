"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

from .base_views import BaseViewSet
from accounting.models import Store,Branch
from accounting.serializers import StoreSerializer,BranchSerializer


class StoreViewSet(BaseViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class BranchViewSet(BaseViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()

