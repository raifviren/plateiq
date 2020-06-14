"""
Created at 13/06/20
@author: virenderkumarbhargav
"""
import os
import re
import uuid

import boto
from boto.s3.key import Key
from django.conf import settings
from django.utils.timezone import now


def upload_image_to(instance, filename):
    """
    @summary: upload_image_to method helps models to upload images to S3

    @param instance: models.Model object
    @param filename: string

    @return: string
    """
    filename, filename_ext = os.path.splitext(filename)
    object_type = instance.__class__.__name__
    return '%s/%s%s%s' % (
        object_type.lower(),
        filename, now().strftime("%Y%m%d%H%M%S%s"),
        filename_ext.lower(),
    )


def s3_upload_file(data, output_filename):
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    k = Key(bucket)
    k.key = 'temp-downloads/{}'.format(uuid.uuid4().hex)
    k.set_contents_from_file(data)

    download_url = k.generate_url(
        expires_in=60,
        response_headers={
            'response-content-type': 'text/csv',
            'response-content-disposition': 'attachment; filename={}'.format(
                output_filename),
        }
    )
    return download_url


def update_selected(instance, data, fields):
    for key in fields:
        setattr(instance, key, data.get(key, getattr(instance, key)))


def is_phone_valid(phone):
    regex_object = re.search(
        "\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$",
        phone)
    return True if regex_object else False
