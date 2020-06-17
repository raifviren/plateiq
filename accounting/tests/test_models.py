"""
Created at 15/06/20
@author: virenderkumarbhargav
Tests core accounting/models
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from django.utils.timezone import now

from accounting.models import Invoice, Branch, Vendor, Store, Organization, User, Document, get_super_user, \
    InvoiceLineItem, Item
from accounting.tests.stub_methods import get_or_create_branch, get_or_create_vendor, create_invoice, create_document, \
    create_item


class InvoiceTestCase(TestCase):  # pylint: disable=too-many-public-methods
    """
    Test cases for creating Invoice model objects
    """

    def setUp(self):
        """
        Make test database ready to run each test
        """
        Vendor.objects.all().delete()
        Invoice.objects.all().delete()
        Store.objects.all().delete()
        Branch.objects.all().delete()
        Organization.objects.all().delete()

    def test_missing_branch(self):
        """
        The branch was not provided
        """
        with self.assertRaises(IntegrityError) as context:
            invoice = Invoice(vendor=get_or_create_vendor(), invoice_num='INV0001',
                              date="2020-06-15",
                              total_amount=100.0, document=create_document())
            invoice.save()
            self.fail("'test_missing_branch' did not get the expected error")
        self.assertTrue('null value in column "branch_id" violates not-null constraint' in str(context.exception))

    def test_missing_vendor(self):
        """
        The vendor was not provided
        """
        branch = get_or_create_branch()
        with self.assertRaises(IntegrityError) as context:
            invoice = Invoice(branch=branch, invoice_num='INV0001',
                              date="2020-06-15",
                              total_amount=100.0, document=create_document())
            invoice.save()
            self.fail("'test_missing_vendor' did not get the expected error")
        self.assertTrue('null value in column "vendor_id" violates not-null constraint' in str(context.exception))

    def test_missing_document(self):
        """
        The document was not provided
        """
        branch = get_or_create_branch()
        with self.assertRaises(IntegrityError) as context:
            invoice = Invoice(branch=branch, vendor=get_or_create_vendor(store=branch.store), invoice_num='INV0001',
                              date="2020-06-15", total_amount=100.0)
            invoice.save()
            self.fail("'test_missing_document' did not get the expected error")
        self.assertTrue('null value in column "document_id" violates not-null constraint' in str(context.exception))

    def test_missing_date(self):
        """
        The date was not provided
        """
        branch = get_or_create_branch()
        with self.assertRaises(IntegrityError) as context:
            invoice = Invoice(branch=branch, vendor=get_or_create_vendor(store=branch.store), invoice_num='INV0001',
                              total_amount=100.0, document=create_document())
            invoice.save()
            self.fail("'test_missing_date' did not get the expected error")
        self.assertTrue('null value in column "date" violates not-null constraint' in str(context.exception))

    def test_missing_invoice_num(self):
        """
        The invoice_num was not provided
        """
        branch = get_or_create_branch()
        with self.assertRaises(ValidationError) as context:
            invoice = Invoice(branch=branch, vendor=get_or_create_vendor(store=branch.store), date="2020-06-15",
                              total_amount=100.0, document=create_document())
            invoice.full_clean()
            invoice.save()
            self.fail("'test_invoice_num' did not get the expected error")
        self.assertTrue("{'invoice_num': ['This field cannot be blank.']}" in str(context.exception))

    def test_missing_total_amount(self):
        """
        The total_amount was not provided
        """
        branch = get_or_create_branch()
        document = create_document()
        with self.assertRaises(IntegrityError) as context:
            invoice = Invoice(branch=branch, vendor=get_or_create_vendor(store=branch.store), invoice_num='INV0001',
                              date="2020-06-15", document=document)
            invoice.save()
            self.fail("'test_missing_total_amount' did not get the expected error")
        self.assertTrue('null value in column "total_amount" violates not-null constraint' in str(context.exception))

    def test_defaults(self):
        """
        Do not provide fields that can be defaulted and test their values
        """
        current_ts = now()
        invoice = create_invoice()
        invoice.save()
        self.assertEqual(False, invoice.is_deleted)
        self.assertNotEqual(None, invoice.created_at)
        self.assertNotEqual(None, invoice.updated_at)
        self.assertGreaterEqual(invoice.created_at, current_ts)
        self.assertGreaterEqual(invoice.updated_at, current_ts)
        self.assertIsInstance(invoice, Invoice)
        self.assertIsInstance(invoice.branch, Branch)
        self.assertIsInstance(invoice.vendor, Vendor)


class DocumentTestCase(TestCase):  # pylint: disable=too-many-public-methods
    """
    Test cases for creating Document model objects
    """

    def setUp(self):
        """
        Make test database ready to run each test
        """
        Document.objects.all().delete()
        User.objects.all().delete()

    def test_missing_file(self):
        """
        The file was not provided
        """
        with self.assertRaises(ValidationError) as context:
            document = Document(created_by=get_super_user())
            document.full_clean()
            document.save()
            self.fail("'test_missing_file' did not get the expected error")
        self.assertTrue("{'file': ['This field cannot be blank.']}" in str(context.exception))

    def test_default_created_by(self):
        """
        The created_by was not provided
        """
        document = Document(file=SimpleUploadedFile("file.txt", b'file_content'))
        document.full_clean()
        document.save()
        self.assertIsInstance(document, Document)
        self.assertIsNotNone(document.created_by)

    def test_defaults(self):
        """
        Do not provide fields that can be defaulted and test their values
        """
        current_ts = now()
        document = create_document()
        document.save()
        self.assertEqual(False, document.is_deleted)
        self.assertEqual(False, document.is_digitized)
        self.assertNotEqual(None, document.created_at)
        self.assertNotEqual(None, document.updated_at)
        self.assertGreaterEqual(document.created_at, current_ts)
        self.assertGreaterEqual(document.updated_at, current_ts)
        self.assertIsInstance(document, Document)


class InvoiceLineItemTestCase(TestCase):  # pylint: disable=too-many-public-methods
    """
    Test cases for creating InvoiceLineItem model objects
    """

    def setUp(self):
        """
        Make test database ready to run each test
        """
        InvoiceLineItem.objects.all().delete()
        Item.objects.all().delete()
        Invoice.objects.all().delete()
        User.objects.all().delete()

    def test_missing_invoice(self):
        """
        The invoice was not provided
        """
        with self.assertRaises(IntegrityError) as context:
            invoice_line_item = InvoiceLineItem(item=create_item(), quantity=10,
                                                price=100.0)
            invoice_line_item.save()
            self.fail("'test_missing_invoice' did not get the expected error")
        self.assertTrue('null value in column "invoice_id" violates not-null constraint' in str(context.exception))

    def test_missing_item(self):
        """
        The item was not provided
        """
        with self.assertRaises(IntegrityError) as context:
            invoice_line_item = InvoiceLineItem(invoice=create_invoice(create_item=False),
                                                quantity=10,
                                                price=100.0)
            invoice_line_item.save()
            self.fail("'test_missing_item' did not get the expected error")
        self.assertTrue('null value in column "item_id" violates not-null constraint' in str(context.exception))

    def test_missing_price(self):
        """
        The price was not provided
        """
        branch = get_or_create_branch()
        with self.assertRaises(ValidationError) as context:
            invoice_line_item = InvoiceLineItem(item=create_item(branch),
                                                invoice=create_invoice(branch=branch,create_item=False),
                                                quantity=10)
            invoice_line_item.full_clean()
            invoice_line_item.save()
            self.fail("'test_missing_price' did not get the expected error")
        self.assertTrue("{'price': ['This field cannot be null.']}" in str(context.exception))

    def test_default_quantity(self):
        """
        The quantity was not provided
        """
        branch = get_or_create_branch()
        invoice_line_item = InvoiceLineItem(item=create_item(branch),
                                            invoice=create_invoice(branch=branch,create_item=False),
                                            price=100.0)
        invoice_line_item.save()
        self.assertIsInstance(invoice_line_item, InvoiceLineItem)

        self.assertEqual(invoice_line_item.quantity, 1)

    def test_defaults(self):
        """
        Do not provide fields that can be defaulted and test their values
        """
        current_ts = now()
        branch = get_or_create_branch()
        invoice_line_item = InvoiceLineItem(item=create_item(branch),
                                            invoice=create_invoice(branch=branch, create_item=False),
                                            price=100.0)
        invoice_line_item.save()
        self.assertEqual(False, invoice_line_item.is_deleted)
        self.assertNotEqual(None, invoice_line_item.created_at)
        self.assertNotEqual(None, invoice_line_item.updated_at)
        self.assertGreaterEqual(invoice_line_item.created_at, current_ts)
        self.assertGreaterEqual(invoice_line_item.updated_at, current_ts)
        self.assertIsInstance(invoice_line_item, InvoiceLineItem)


class ItemTestCase(TestCase):  # pylint: disable=too-many-public-methods
    """
    Test cases for creating Item model objects
    """

    def setUp(self):
        """
        Make test database ready to run each test
        """
        Item.objects.all().delete()

    def test_missing_branch(self):
        """
        The branch was not provided
        """
        with self.assertRaises(IntegrityError) as context:
            item = Item(name="item 1", price=100.0)
            item.save()
            self.fail("'test_missing_branch' did not get the expected error")
        self.assertTrue('null value in column "branch_id" violates not-null constraint' in str(context.exception))

    def test_blank_name(self):
        """
        The name was not provided
        """
        with self.assertRaises(ValidationError) as context:
            item = Item(branch=get_or_create_branch(),
                        price=100.0)
            item.full_clean()
            item.save()
            self.fail("'test_blank_name' did not get the expected error")
        self.assertTrue("{'name': ['This field cannot be blank.']}" in str(context.exception))

    def test_missing_price(self):
        """
        The price was not provided
        """
        with self.assertRaises(ValidationError) as context:
            item = Item(branch=get_or_create_branch(),
                        name="item 1")
            item.full_clean()
            item.save()
            self.fail("'test_missing_price' did not get the expected error")
        self.assertTrue("{'price': ['This field cannot be null.']}" in str(context.exception))

    def test_defaults(self):
        """
        Do not provide fields that can be defaulted and test their values
        """
        current_ts = now()
        item = create_item()
        item.save()
        self.assertIsInstance(item, Item)
        self.assertEqual(False, item.is_deleted)
        self.assertNotEqual(None, item.created_at)
        self.assertNotEqual(None, item.updated_at)
        self.assertGreaterEqual(item.created_at, current_ts)
        self.assertGreaterEqual(item.updated_at, current_ts)
