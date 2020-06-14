"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

from rest_framework import serializers

from accounting.constants import CONST_ORGANIZATION_TYPE
from accounting.exceptions import InvalidInputError
from accounting.models import Store, Branch, Organization, User
from .user_serializers import BasicUserReadSerializer


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
    owner = serializers.CharField(required=True)

    class Meta:
        model = Store
        fields = ('organization', 'owner')

    def create(self, validated_data):
        organization_data = validated_data.get('organization')
        organization = Organization.objects.create(**organization_data)
        owner = User.objects.get(pk=validated_data.get('owner'))
        if owner is None:
            raise InvalidInputError("Owner does not exists.")
        store = Store.objects.create(organization=organization, owner=owner)
        return store

    def to_representation(self, instance):
        data = _instance_repr(instance)
        data['organization'] = OrganisationSerializer(instance.organization).data
        data['owner'] = BasicUserReadSerializer(instance.owner).data
        return data


class BranchSerializer(serializers.ModelSerializer):
    organization = OrganisationSerializer(required=True)
    store = serializers.CharField(required=True)

    class Meta:
        model = Branch
        fields = ('store', 'organization')

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
