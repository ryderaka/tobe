# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class TodoUser(models.Model):
    phone = models.BigIntegerField(blank=True, unique=True)
    name = models.CharField(max_length=60, blank=True, unique=False)
    # slug = AutoSlugField(populate_from='name', editable=False, always_update=True)
    email = models.EmailField(unique=False, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(blank=True, null=True)
    auth_token = models.CharField(max_length=255, blank=True, null=True)
    # add device registration token
    # auth_token = models.ForeignKey(TodoAuthtoken)

    def __str__(self):
        return self.name
        # return '{}{}'.format(self.name, self.auth_token)


class TodoList(models.Model):
    title = models.CharField(max_length=140, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    created_by = models.ForeignKey(TodoUser, blank=True, null=True, related_name='todo_created_by')
    created_date = models.DateTimeField(default=timezone.now)
    assigned_to = models.ForeignKey(TodoUser, blank=True, null=True, related_name='todo_assigned_to')
    assigned_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True, )
    isaccepted = models.BooleanField(default=False)
    isdeleted = models.BooleanField(default=False)
    iscompleted = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


# class TodoAuthtoken(models.Model):
#     token = models.CharField(max_length=56)

#
# @receiver(post_save, sender=TodoUser)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
