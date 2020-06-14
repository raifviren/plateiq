"""
Created at 14/06/20
@author: virenderkumarbhargav
"""
from accounting import views
# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()  # pylint: disable=invalid-name
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
