# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-12 14:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20170730_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login',
            old_name='nt',
            new_name='cnn',
        ),
    ]
