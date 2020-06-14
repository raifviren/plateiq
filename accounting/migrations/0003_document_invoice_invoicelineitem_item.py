# Generated by Django 3.0.7 on 2020-06-14 16:59

import accounting.utils
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20200614_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('file', models.FileField(upload_to=accounting.utils.upload_image_to)),
                ('is_digitized', models.BooleanField(default=False)),
                ('meta_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('invoice_num', models.CharField(max_length=30, unique=True, verbose_name='Invoice Number')),
                ('date', models.DateField()),
                ('total_amount', models.FloatField(max_length=99999999.99)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Branch')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.Document')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Vendor')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('price', models.FloatField(max_length=99999.99)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Branch')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvoiceLineItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField(max_length=99999.99)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Invoice')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Item')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
