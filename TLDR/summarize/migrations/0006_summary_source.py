# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarize', '0005_summary_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='source',
            field=models.TextField(default='', null=True),
        ),
    ]
