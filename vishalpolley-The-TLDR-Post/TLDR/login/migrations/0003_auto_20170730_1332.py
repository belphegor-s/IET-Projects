# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-30 13:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20170730_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='nol',
            field=models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(5)]),
        ),
    ]