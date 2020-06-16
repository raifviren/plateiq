"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

import json

from django.db import transaction
from rest_framework import serializers

import accounting
from accounting.exceptions import InvalidInputError
from accounting.models import Document, Invoice, User, Branch, Item, InvoiceLineItem, Vendor
from accounting.serializers.user_serializers import BasicUserReadSerializer, UserSerializer, VendorSerializer
from accounting.utils import DocumentJSONEncoder, update_selected


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
        fields = ('id', 'is_digitized', 'file', 'created_by', 'meta_data')

    @transaction.atomic
    def update(self, instance, validated_data):
        update_selected(instance, validated_data, ['is_digitized'])
        instance.save()
        return instance


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = '__all__'


class InvoiceItemSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    name = serializers.CharField(max_length=30, required=True)
    price = serializers.FloatField(required=True)
    quantity = serializers.IntegerField(required=True)


class InvoiceSerializer(serializers.Serializer):
    branch_id = serializers.UUIDField(required=True)
    vendor = UserSerializer(required=True)
    invoice_num = serializers.CharField(max_length=30, required=True)
    date = serializers.DateField(required=True)
    total_amount = serializers.FloatField(required=True)
    items = InvoiceItemSerializer(many=True, required=True)
    document_id = serializers.UUIDField(required=True)

    @transaction.atomic
    def create(self, validated_data):
        vendor_data = validated_data.get('vendor')
        vendor_user = User.get_user_by_mobile(vendor_data['mobile'])
        if vendor_user is None:
            new_vendor_user = User.objects.create(**vendor_data)
        branch = Branch.objects.get(pk=validated_data.get('branch_id'))
        if branch is None:
            raise InvalidInputError("Branch does not exists.")
        if vendor_user is None:
            vendor = Vendor.objects.create(user=new_vendor_user, store=branch.store)
        else:
            vendor = Vendor.objects.filter(user=vendor_user).first()
        document = Document.objects.get(pk=validated_data.get('document_id'))
        if document is None:
            raise InvalidInputError("Document does not exists.")
        document.meta_data = json.loads(json.dumps(validated_data, cls=DocumentJSONEncoder))
        document.is_digitized = True
        document.save()
        validated_data.pop('vendor')
        validated_data.pop('items')
        invoice = Invoice.objects.create(branch=branch, vendor=vendor, **validated_data)
        items_data = validated_data.get('items')
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

    @transaction.atomic
    def update(self, instance, validated_data):
        update_selected(instance, validated_data, ['invoice_num', 'date', 'total_amount'])
        InvoiceLineItem.objects.filter(invoice=instance).delete()
        items_data = validated_data.get('items')
        for item_data in items_data:
            item = Item.objects.filter(name=item_data['name'], branch=instance.branch).first()
            if item is None:
                item = Item.objects.create(name=item_data['name'], branch=instance.branch, price=item_data['price'])
            else:
                item.price = item_data['price']
            item.save()
            InvoiceLineItem.objects.create(invoice=instance, item=item, quantity=item_data['quantity'],
                                           price=item_data['price'])
        instance.save()
        return instance

    def to_representation(self, instance):
        data = _instance_repr(instance)
        data['branch'] = accounting.serializers.BranchSerializer(instance.branch).data
        data['vendor'] = VendorSerializer(instance.vendor).data
        items = []
        for invoice_line_item in instance.items_rels.all():
            items.append(InvoiceLineItemSerializer(invoice_line_item).data)
        data['items'] = items
        return data


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
