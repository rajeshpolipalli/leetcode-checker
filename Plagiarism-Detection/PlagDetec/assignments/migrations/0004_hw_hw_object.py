# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-20 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_auto_20180420_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='hw',
            name='hw_object',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
