"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from __future__ import absolute_import

from django.conf.urls import url, include
from accounting import views

# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.routers import SimpleRouter


app_name = 'community'

router = SimpleRouter()  # pylint: disable=invalid-name
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'stores', views.StoreViewSet, basename='stores')
router.register(r'branches', views.BranchViewSet, basename='branches')
router.register(r'documents', views.DocumentViewSet, basename='documents')
router.register(r'invoices', views.InvoiceViewSet, basename='invoices')

urlpatterns = [
    url(r'^', include(router.urls)),
]
