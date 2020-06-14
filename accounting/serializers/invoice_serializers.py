"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

from rest_framework import serializers

import accounting
from accounting.exceptions import InvalidInputError
from accounting.models import Document, Invoice, User, Branch, Item, InvoiceLineItem, Vendor
from accounting.serializers.user_serializers import BasicUserReadSerializer, UserSerializer, VendorSerializer


def _instance_repr(instance):
    data = {}
    for field in instance._meta.concrete_fields:  # pylint: disable=old-style-class, protected-access
        if field.name == 'image' or field.name == 'file' or field.name == 'photo':
            data[field.name] = instance.image.url if instance.image else ""
        else:
            data[field.name] = field.value_from_object(instance)
    return data


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    created_by = BasicUserReadSerializer(read_only=True)
    is_digitized = serializers.BooleanField()
    meta_data = serializers.JSONField(read_only=True)

    class Meta:
        model = Document
        fields = ('file', 'created_by', 'is_digitized', 'meta_data')


class InvoiceLineItemSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    name = serializers.CharField(max_length=30, required=True)
    price = serializers.FloatField(required=True)
    quantity = serializers.IntegerField(required=True)


class InvoiceSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    branch = serializers.CharField(required=True)
    vendor = UserSerializer(required=True)
    invoice_num = serializers.CharField(max_length=30, required=True)
    date = serializers.DateField(required=True)
    total_amount = serializers.FloatField(required=True)
    items = InvoiceLineItemSerializer(many=True, required=True)
    document = DocumentSerializer(read_only=True)

    # class Meta:
    #     model = Invoice
    #     fields = ('branch', 'vendor', 'invoice_num', 'date', 'total_amount', 'document', 'items')

    def create(self, validated_data):
        print(validated_data)
        vendor_data = validated_data.get('vendor')
        vendor_user = User.objects.create(**vendor_data)
        validated_data.pop('vendor')
        branch = Branch.objects.get(pk=validated_data.get('branch'))
        if branch is None:
            raise InvalidInputError("Branch does not exists.")
        validated_data.pop('branch')
        vendor = Vendor.objects.create(user=vendor_user, store=branch.store)
        items_data = validated_data.get('items')
        validated_data.pop('items')
        invoice = Invoice.objects.create(branch=branch, vendor=vendor, **validated_data)
        for item_data in items_data:
            item = Item.objects.filter(name=item_data['name'], branch=branch).first()
            if item is None:
                item = Item.objects.create(name=item_data['name'], branch=branch, price=item_data['price'])
            else:
                item.price = item_data['price']
            item.save()
            InvoiceLineItem.objects.create(invoice=invoice, item=item, quantity=item_data['quantity'],
                                           price=item_data['price'])
        return invoice

    def to_representation(self, instance):
        data = _instance_repr(instance)
        data['branch'] = accounting.serializers.BranchSerializer(instance.branch).data
        data['vendor'] = VendorSerializer(instance.vendor).data
        return data
