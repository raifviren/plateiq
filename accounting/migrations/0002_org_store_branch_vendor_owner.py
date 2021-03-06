# Generated by Django 3.0.7 on 2020-06-14 14:33

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import accounting.utils


class Migration(migrations.Migration):
    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name')),
                ('logo', models.ImageField(blank=True, help_text='Organization logo used for display', null=True,
                                           upload_to=accounting.utils.upload_image_to)),
                ('type',
                 models.CharField(blank=True, choices=[('store', 'store'), ('branch', 'branch')], max_length=20)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Merchant',
                'verbose_name_plural': 'Merchants',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('organization',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounting.Organization')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores',
                                            to='accounting.Owner')),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendors',
                                            to='accounting.Store')),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='branch',
            name='organization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounting.Organization'),
        ),
        migrations.AddField(
            model_name='branch',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches',
                                    to='accounting.Store'),
        ),
    ]
