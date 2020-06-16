"""
Created at 16/06/20
@author: virenderkumarbhargav
Test for accounting/views
"""
# pylint: disable= too-many-lines
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounting.models import User, Invoice, Document, Store
from accounting.tests.stub_methods import create_invoice_payload, create_invoice, create_document


class TestInvoiceViewSet(APITestCase):
    """
    Test InvoiceVieSet GET,POST and PUT methods
    """

    def setUp(self):
        """
        Dummy method to create AUTH_USER_MODEL
        """
        User.objects.all().delete()
        Invoice.objects.all().delete()
        self.mobile = '+9199999999'
        self.password = 'plateiqtest'
        user_model = apps.get_model(settings.AUTH_USER_MODEL)
        user_obj = user_model.objects.create(mobile=self.mobile)
        user_obj.set_password(self.password)
        user_obj.is_staff = True
        user_obj.is_superuser = True
        user_obj.save()
        self.user = user_obj
        self.client = APIClient()
        self.url = '/api/v1/invoices/'

    def test_empty_get(self):
        """
        TestCase: What if a user send valid session in headers and makes get request
        ExpectedOutput: Request must get status.HTTP_200_OK status code
        User: staff user
        """
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual({u'count': 0,
                              u'previous': None,
                              u'results': [],
                              u'next': None}, response.json())

    def test_valid_post_get(self):
        """
        TestCase: What if a user send valid session in headers and upload valid content
        ExpectedOutput: Request must get status.HTTP_201_CREATED status code
        User: superuser
        """
        # Add permissions to access resources
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)

        response = self.client.post(self.url, create_invoice_payload(),
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test get call as well
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 1)

    def test_valid_put(self):
        """
        TestCase: What if a user send valid session in headers and update valid content
        ExpectedOutput: Request must get status.HTTP_200_Ok status code
        User: superuser
        """
        # Add permissions to access resources
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)
        invoice = create_invoice()
        url = self.url + str(invoice.pk) + '/'
        update_payload = {
            "invoice_num": "INV0001",
            "date": "2020-06-15",
            "total_amount": "2000.0",
            "items": [
                {
                    "name": "Item 3",
                    "price": "100.0",
                    "quantity": "10"
                },
                {
                    "name": "Item 4",
                    "price": "100.0",
                    "quantity": "10"
                }
            ]
        }

        res = self.client.put(url, update_payload,
                              format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        response = res.json()
        self.assertEqual(response.get('invoice_num'), "INV0001")
        self.assertEqual(response.get('date'), "2020-06-15")
        self.assertEqual(response.get('total_amount'), 2000.0)
        items = response.get('items')
        self.assertEqual(len(items), 2)


class TestDocumentViewSet(APITestCase):
    """
    Test DocumentViewSet GET, POST and PUT methods
    """

    def setUp(self):
        """
        Dummy method to create AUTH_USER_MODEL
        """
        User.objects.all().delete()
        Document.objects.all().delete()
        self.mobile = '+9199999999'
        self.password = 'plateiqtest'
        user_model = apps.get_model(settings.AUTH_USER_MODEL)
        user_obj = user_model.objects.create(mobile=self.mobile)
        user_obj.set_password(self.password)
        user_obj.is_staff = True
        user_obj.is_superuser = True
        user_obj.save()
        self.user = user_obj
        self.client = APIClient()
        self.url = '/api/v1/documents/'

    def test_empty_get(self):
        """
        TestCase: What if a user send valid session in headers and makes get request
        ExpectedOutput: Request must get status.HTTP_200_OK status code
        User: staff user
        """
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual({u'count': 0,
                              u'previous': None,
                              u'results': [],
                              u'next': None}, response.json())

    def test_valid_post_get(self):
        """
        TestCase: What if a user send valid session in headers and upload valid content
        ExpectedOutput: Request must get status.HTTP_201_CREATED status code
        User: superuser
        """
        # Add permissions to access resources
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)

        response = self.client.post(self.url, {'file': SimpleUploadedFile("file.txt", b'file_content')},
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test get call as well
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 1)

    def test_valid_put(self):
        """
        TestCase: What if a user send valid session in headers and update valid content
        ExpectedOutput: Request must get status.HTTP_200_Ok status code
        User: superuser
        """
        # Add permissions to access resources
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)
        document = create_document()
        url = self.url + str(document.pk) + '/'
        res = self.client.put(url, {'is_digitized': True},
                              format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        response = res.json()
        self.assertEqual(response.get('is_digitized'), True)
        self.assertEqual(response.get('id'), str(document.pk))


class TestStoreViewSet(APITestCase):
    """
    Test DocumentViewSet GET, POST methods
    """

    def setUp(self):
        """
        Dummy method to create AUTH_USER_MODEL
        """
        User.objects.all().delete()
        Store.objects.all().delete()
        self.mobile = '+9199999999'
        self.password = 'plateiqtest'
        user_model = apps.get_model(settings.AUTH_USER_MODEL)
        user_obj = user_model.objects.create(mobile=self.mobile)
        user_obj.set_password(self.password)
        user_obj.is_staff = True
        user_obj.is_superuser = True
        user_obj.save()
        self.user = user_obj
        self.client = APIClient()
        self.url = '/api/v1/stores/'

    def test_empty_get(self):
        """
        TestCase: What if a user send valid session in headers and makes get request
        ExpectedOutput: Request must get status.HTTP_200_OK status code
        User: staff user
        """
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual({u'count': 0,
                              u'previous': None,
                              u'results': [],
                              u'next': None}, response.json())

    def test_valid_post_get(self):
        """
        TestCase: What if a user send valid session in headers and upload valid content
        ExpectedOutput: Request must get status.HTTP_201_CREATED status code
        User: superuser
        """
        # Add permissions to access resources
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=self.mobile, password=self.password)
        # owner =
        store_payload = {
            "organization": {
                "name": "Ente Kada",
                "type": "store"
            },
            "owner": {
                "first_name": "owner",
                "last_name": "John Doe",
                "mobile": "+9188888888",
                "user_type": "owner"
            }
        }

        response = self.client.post(self.url, store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test get call as well
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 1)

