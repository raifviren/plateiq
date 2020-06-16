"""
Created at 15/06/20
@author: virenderkumarbhargav
"""
import random
import string

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.utils.timezone import now

from accounting.models import Branch, Store, Organization, get_super_user, Vendor, Invoice, InvoiceLineItem, Item, \
    Document, Owner


@transaction.atomic
def get_or_create_store():
    organization, _ = Organization.objects.get_or_create(
        name='PlateIq Store',
        type='store'
    )
    superuser = get_super_user()
    owner, _ = Owner.objects.get_or_create(user=superuser)
    store, _ = Store.objects.get_or_create(
        organization=organization,
        owner=owner
    )
    return store


@transaction.atomic
def get_or_create_branch():
    store = get_or_create_store()
    organization, _ = Organization.objects.get_or_create(
        name='PlateIq Branch',
        type='branch'
    )
    branch, _ = Branch.objects.get_or_create(
        store=store,
        organization=organization
    )
    return branch


@transaction.atomic
def get_or_create_vendor(store=None):
    if store is None:
        store = get_or_create_store()
    superuser = get_super_user()
    vendor, _ = Vendor.objects.get_or_create(user=superuser, store=store)
    return vendor


def create_document():
    superuser = get_super_user()
    file = SimpleUploadedFile("file.txt", b'file_content')
    document, _ = Document.objects.get_or_create(file=file, created_by=superuser)
    return document


@transaction.atomic
def create_invoice(branch=None, vendor=None, invoice_num=None,create_item=True):
    if branch is None:
        branch = get_or_create_branch()
    if vendor is None:
        vendor = get_or_create_vendor(store=branch.store)
    if invoice_num is None:
        invoice_num = 'INV' + ''.join([random.choice(string.digits) for _ in range(6)])
    invoice_data = {
        "invoice_num": invoice_num,
        "date": now().strftime('%Y-%m-%d'),
        "total_amount": "100.0",
    }
    item_data = {"items": [
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
    ]}
    invoice = Invoice.objects.create(branch=branch, vendor=vendor, document=create_document(), **invoice_data)
    if not create_item:
        return invoice
    items_data = item_data.get('items')
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


def create_item(branch=None):
    if branch is None:
        branch = get_or_create_branch()
    item, _ = Item.objects.get_or_create(name="Item 1", branch=branch, price=10.0)
    return item


def create_invoice_payload(branch=None, invoice_num=None):
    if branch is None:
        branch = get_or_create_branch()
    if invoice_num is None:
        invoice_num = 'INV' + ''.join([random.choice(string.digits) for _ in range(6)])
    payload = {
        "document_id": str(create_document().id),
        "vendor": {
            "first_name": "John",
            "last_name": "Doe",
            "mobile": "+9188888872",
            "user_type": "vendor"
        },
        "branch_id": str(branch.id),
        "invoice_num": invoice_num,
        "date": now().strftime('%Y-%m-%d'),
        "total_amount": "100.0",
        "items": [
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
    }
    return payload


