# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-01 16:25
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filings', '0007_auto_20170401_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='filing',
            name='date_submitted',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='filing',
            name='documents',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None),
        ),
    ]