# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tobe', '0002_auto_20171003_0611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='todolist',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='todo_assigned_to', to='tobe.TodoUser'),
        ),
        migrations.RemoveField(
            model_name='todolist',
            name='created_by',
        ),
        migrations.AddField(
            model_name='todolist',
            name='created_by',
            field=models.ManyToManyField(related_name='todo_created_by', to='tobe.TodoUser'),
        ),
    ]
