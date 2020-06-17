"""
Created at 16/06/20
@author: virenderkumarbhargav
Tests for accounting/serializers
"""
# -*- coding: utf-8 -*-

# pylint: disable=C0302
from __future__ import unicode_literals

import random
import string
from uuid import uuid4 as uuidv4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from accounting.models import Invoice, Document
from accounting.serializers import InvoiceSerializer, DocumentSerializer


class InvoiceSerializerTest(TestCase):
    """
    Test cases to test InvoiceSerializer
    """

    @staticmethod
    def setUp(**kwargs):
        """
        Clean database before each test
        :param **kwargs:
        """
        Invoice.objects.all().delete()

    @staticmethod
    def get_vendor_data():
        return {
            "first_name": "John",
            "last_name": "Doe",
            "mobile": "+9188888872",
            "user_type": "vendor"
        }

    @staticmethod
    def get_invoice_num():
        return 'INV' + ''.join([random.choice(string.digits) for _ in range(6)])

    @staticmethod
    def get_items_data():
        return [
            {
                "name": "Item 1",
                "price": "10.0",
                "quantity": "5"
            },
            {
                "name": "Item 2",
                "price": "10.0",
                "quantity": "5"
            }
        ]

    def test_empty_data(self):
        """
        Verify failure with empty data
        """
        serializer = InvoiceSerializer(data={})
        self.assertEqual(False, serializer.is_valid())

    def test_invalid_branch_id(self):
        """
        the "branch_id" should be a valid uuid. Other values must be treated as invalid values
        """
        serializer = InvoiceSerializer(data={'vendor': self.get_vendor_data(),
                                             'invoice_num': self.get_invoice_num(),
                                             'date': "2020-06-14",
                                             'total_amount': "100.0",
                                             'items': self.get_items_data(),
                                             'document_id': str(uuidv4())
                                             })
        self.assertEqual(serializer.is_valid(), False)
        self.assertDictEqual(serializer.errors,
                             {'branch_id': [ErrorDetail(string='This field is required.', code='required')]})

    def test_unknown_fields(self):
        """
        Verify failure with unknown fields
        """
        serializer = InvoiceSerializer(data={'some_field': 'some_value'})
        self.assertEqual(False, serializer.is_valid())

    def test_invalid_date(self):
        """
        Verify failure with invalid values for date field
        """
        serializer = InvoiceSerializer(data={'branch_id': str(uuidv4()),
                                             'vendor': self.get_vendor_data(),
                                             'invoice_num': self.get_invoice_num(),
                                             'date': "2020",
                                             'total_amount': "100.0",
                                             'items': self.get_items_data(),
                                             'document_id': str(uuidv4())
                                             })
        self.assertEqual(False, serializer.is_valid())

    def test_invalid_total_amount(self):
        """
        Verify failure with invalid values for date field
        """
        serializer = InvoiceSerializer(data={'branch_id': str(uuidv4()),
                                             'vendor': self.get_vendor_data(),
                                             'invoice_num': self.get_invoice_num(),
                                             'date': "2020",
                                             'total_amount': "abc",
                                             'items': self.get_items_data(),
                                             'document_id': str(uuidv4())
                                             })
        self.assertEqual(False, serializer.is_valid())

    def test_valid_data(self):
        """
        Verify successful validation of valid input data
        """
        serializer = InvoiceSerializer(data={'branch_id': str(uuidv4()),
                                             'vendor': self.get_vendor_data(),
                                             'invoice_num': self.get_invoice_num(),
                                             'date': "2020-06-14",
                                             'total_amount': "100.0",
                                             'items': self.get_items_data(),
                                             'document_id': str(uuidv4())
                                             })
        self.assertEqual(True, serializer.is_valid())
        self.assertEqual(100.0, serializer.validated_data['total_amount'])


class DocumentSerializerTest(TestCase):
    """
    Test cases to test DocumentSerializer
    """

    @staticmethod
    def setUp(**kwargs):
        """
        Clean database before each test
        :param **kwargs:
        """
        Document.objects.all().delete()

    def test_empty_data(self):
        """
        Verify failure with empty data
        """
        serializer = DocumentSerializer(data={})
        self.assertEqual(False, serializer.is_valid())

    def test_missing_file(self):
        """
        the "file" should be a valid file. Other values must be treated as invalid values
        """
        serializer = DocumentSerializer(data={'is_digitized': False})
        self.assertEqual(serializer.is_valid(), False)
        self.assertDictEqual(serializer.errors,
                             {'file': [ErrorDetail(string='No file was submitted.', code='required')]})

    def test_unknown_fields(self):
        """
        Verify failure with unknown fields
        """
        serializer = InvoiceSerializer(data={'some_field': 'some_value'})
        self.assertEqual(False, serializer.is_valid())

    def test_invalid_is_digitized(self):
        """
        Verify failure with invalid values for is_digitized field
        """
        serializer = DocumentSerializer(data={'file': SimpleUploadedFile("file.txt", b'file_content'),
                                              'is_digitized': "sasa"})
        self.assertEqual(False, serializer.is_valid())

    def test_invalid_file(self):
        """
        Verify failure with invalid values for file field
        """
        serializer = DocumentSerializer(data={'file': "qwe",
                                              'is_digitized': "sasa"})
        self.assertEqual(False, serializer.is_valid())

    def test_valid_data(self):
        """
        Verify successful validation of valid input data
        """
        serializer = DocumentSerializer(data={'file': SimpleUploadedFile("file.txt", b'file_content'),
                                              'is_digitized': False})
        self.assertEqual(True, serializer.is_valid())
        self.assertEqual(False, serializer.validated_data['is_digitized'])
