# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tobe', '0006_auto_20171004_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todouser',
            name='slug',
        ),
        migrations.AlterField(
            model_name='todouser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
