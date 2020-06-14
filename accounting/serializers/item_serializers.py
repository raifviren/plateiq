"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

from rest_framework import serializers

from accounting.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
