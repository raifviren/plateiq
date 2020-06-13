import logging
import os
import uuid


import boto
# import requests
from boto.s3.key import Key
from django.conf import settings
from django.db import transaction
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