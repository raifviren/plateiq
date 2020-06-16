"""
Created at 15/06/20
@author: virenderkumarbhargav
"""
import random
import string

from django.db import transaction

from accounting.models import Branch, Organization, Store, get_super_user


@transaction.atomic
def get_or_create_store():
    organization, _ = Organization.objects.get_or_create(
        name='PlateIq Store',
        type='store'
    )
    superuser = get_super_user()
    store, _ = Store.objects.get_or_create(
        organization=organization,
        owner=superuser
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


def get_dummy_invoice_data():
    try:
        branch = get_or_create_branch()
        invoice_num = 'INV' + ''.join([random.choice(string.digits) for _ in range(6)])
        return {
            "vendor": {
                "first_name": "John",
                "last_name": "Doe",
                "mobile": "+9188888872",
                "user_type": "vendor"
            },
            "branch": str(branch.id),
            "invoice_num": invoice_num,
            "date": "2020-06-14",
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
    except Exception as e:
        print(e)
        raise e
