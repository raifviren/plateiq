"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

from django.db import transaction
from rest_framework import serializers

from accounting.constants import CONST_ORGANIZATION_TYPE
from accounting.exceptions import InvalidInputError
from accounting.models import Store, Branch, Organization, User, Owner
from .user_serializers import BasicUserReadSerializer, UserSerializer, OwnerSerializer


def _instance_repr(instance):
    data = {}
    for field in instance._meta.concrete_fields:  # pylint: disable=old-style-class, protected-access
        if field.name == 'image' or field.name == 'file' or field.name == 'photo':
            data[field.name] = instance.image.url if instance.image else ""
        else:
            data[field.name] = field.value_from_object(instance)
    return data


class OrganisationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, required=True)
    logo = serializers.FileField(required=False)
    type = serializers.ChoiceField(choices=CONST_ORGANIZATION_TYPE, default="branch")

    class Meta:
        model = Organization
        fields = ('name', 'logo', 'type')


class StoreSerializer(serializers.ModelSerializer):
    organization = OrganisationSerializer(required=True)
    owner = UserSerializer(required=True)

    class Meta:
        model = Store
        fields = ('organization', 'owner')

    @transaction.atomic
    def create(self, validated_data):
        organization_data = validated_data.get('organization')
        organization = Organization.objects.create(**organization_data)
        owner_data = validated_data.get('owner')
        owner_user = User.get_user_by_mobile(owner_data['mobile'])
        if owner_user is None:
            new_owner_user = User.objects.create(**owner_data)
            owner = Owner.objects.create(user=new_owner_user)
        else:
            owner = Owner.objects.filter(user=owner_user).first()
        store = Store.objects.create(organization=organization, owner=owner)
        return store

    def to_representation(self, instance):
        data = _instance_repr(instance)
        data['organization'] = OrganisationSerializer(instance.organization).data
        data['owner'] = OwnerSerializer(instance.owner).data
        return data


class BranchSerializer(serializers.ModelSerializer):
    organization = OrganisationSerializer(required=True)
    store = serializers.CharField(required=True)

    class Meta:
        model = Branch
        fields = ('store', 'organization')

    @transaction.atomic
    def create(self, validated_data):
        organization_data = validated_data.get('organization')
        organization = Organization.objects.create(**organization_data)
        store = Store.objects.get(pk=validated_data.get('store'))
        if store is None:
            raise InvalidInputError("Store does not exists.")
        branch = Branch.objects.create(organization=organization, store=store)
        return branch

    def to_representation(self, instance):
        data = _instance_repr(instance)
        data['organization'] = OrganisationSerializer(instance.organization).data
        data['store'] = StoreSerializer(instance.store).data
        return data
