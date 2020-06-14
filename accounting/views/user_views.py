"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.utils import IntegrityError
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination

from accounting.exceptions import BaseInputError
from accounting.models import User
from accounting.response import ResponseWrapper, ErrorTemplate
from accounting.serializers import UserReadSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = (AnonCreateAndUpdateOwnerOnly, IsOwnerOrReadOnly)
    PageNumberPagination.page_size = 10
    pagination_class = PageNumberPagination

    def get_serializer_class(self, *args, **kwargs):
        """
        Return serializer according to the request.method
        """
        if self.request.method == 'GET':
            return UserReadSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Only superuser can access all users.
        """
        # if self.request.user.is_superuser:
        #     return User.objects.all()
        # return User.objects.filter(is_superuser=False)
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Overwrites default create method.
        """
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return ResponseWrapper.error_serializer_response(status.HTTP_400_BAD_REQUEST, serializer)
        try:
            user = serializer.save()
            if user is None:
                return ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.INVALID_REQUEST_BODY,
                                                      {})
            result = UserReadSerializer(user).data
            # result.update({'auth_token': user.get_or_create_jwt_authtoken()})
            return ResponseWrapper.response(result, status=status.HTTP_200_OK)
        except IntegrityError as exception:
            return ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.USER_ALREADY_EXISTS,
                                                  exception.args[0])
        except BaseInputError as exception:
            return ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.INVALID_REQUEST_BODY,
                                                  exception.args[0])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return ResponseWrapper.error_serializer_response(status.HTTP_400_BAD_REQUEST, serializer)
        try:
            result = serializer.update(instance=instance, validated_data=request.data)
            data = UserReadSerializer(result).data
            return ResponseWrapper.response(data, status.HTTP_201_CREATED)
        except BaseInputError as exception:
            return ResponseWrapper.error_response(status.HTTP_400_BAD_REQUEST, ErrorTemplate.INVALID_REQUEST_BODY,
                                                  exception.args[0])
