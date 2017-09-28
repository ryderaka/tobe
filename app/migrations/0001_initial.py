# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 10:43
from __future__ import unicode_literals

import autoslug.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('description', models.CharField(max_length=512)),
                ('created_date', models.DateField(default=datetime.datetime.now)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=None)),
                ('completed_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TodoUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField()),
                ('name', models.CharField(max_length=60)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='assigned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_created_by', to='app.TodoUser'),
        ),
        migrations.AddField(
            model_name='item',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_assigned_to', to='app.TodoUser'),
        ),
        migrations.AddField(
            model_name='item',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TodoUser'),
        ),
    ]
