"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import unicode_literals

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounting.constants import CONST_USER_TYPE
from accounting.exceptions import InvalidInputError
from accounting.models import User, Vendor, Owner
from accounting.utils import update_selected, is_phone_valid


class BasicUserReadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    """
    Model Serializer for to be used only for sending asic detail of user.
    This should be use for read only purpose.
    """

    class Meta:  # pylint: disable=old-style-class,no-init,too-few-public-methods
        """Meta of the serializer"""
        model = User
        fields = ('id', 'name', 'photo')

    def get_name(self, obj):
        return obj.get_full_name


class UserReadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    """
    Model Serializer for User model.

    This should be use for read only purpose.
    """

    class Meta:  # pylint: disable=old-style-class,no-init,too-few-public-methods
        """Meta of the serializer"""
        model = User
        exclude = ('password', 'last_login', 'groups', 'user_permissions', 'first_name', 'last_name')

    def get_name(self, obj):
        return obj.get_full_name


class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for User model
    Used for user creation and updation
    """
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    mobile = serializers.CharField(required=True)
    country_code = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    user_type = serializers.ChoiceField(choices=CONST_USER_TYPE, default="owner")

    class Meta:  # pylint: disable=old-style-class,no-init,too-few-public-methods
        """ Meta of the serializer """
        model = User
        fields = ('mobile', 'first_name', 'last_name', 'email', 'photo', 'country_code', 'user_type')

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        update_selected(instance, validated_data, ['first_name', 'last_name', 'country_code'])
        instance.photo = validated_data.get('photo', instance.photo)
        mobile = validated_data.get('mobile', None)
        email = validated_data.get('email', None)
        if mobile and mobile != instance.mobile:
            user = User.get_user_by_mobile(mobile)
            if user is not None:
                raise InvalidInputError("Mobile number already exists.")
            else:
                instance.mobile = mobile
                instance.is_phone_verified = False
        if email and email != instance.email:
            user = User.get_user_by_email(email)
            if user is not None:
                raise InvalidInputError("Email already exits.w")
            else:
                instance.email = email
        instance.save()
        return instance

    def validate_mobile(self, mobile):  # pylint: disable=arguments-differ
        """
        Check whether phone is in valid format and is not already taken by someone else.
        """
        if not is_phone_valid(mobile):
            raise ValidationError('"{0}" should be in format +919999999999(15 digits allowed)'.format(mobile))
        return mobile


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    # store = StoreSerializer(required=True)

    class Meta:
        model = Vendor
        fields = ('user', 'store')

    def create(self, validated_data):
        pass


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    # store = StoreSerializer(required=True)

    class Meta:
        model = Owner
        fields = '__all__'

    def create(self, validated_data):
        pass
