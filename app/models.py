from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import Group
from autoslug import AutoSlugField
from django.conf import settings

# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class TodoUser(models.Model):
    phone = models.IntegerField()
    name = models.CharField(max_length=60)
    slug = AutoSlugField(populate_from='name', editable=False, always_update=True)
    group = models.ForeignKey(Group)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    def incomplete_tasks(self):
        # Count all incomplete tasks on the current User instance
        return Item.objects.filter(list=self, completed=0)

    def complete_tasks(self):
        # Count all complete tasks on the current User instance
        return Item.objects.filter(list=self, completed=1)

    class Meta:
        ordering = ["name"]


class Item(models.Model):
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=512)
    list = models.ForeignKey(TodoUser)
    created_date = models.DateField(default=datetime.datetime.now, blank=False)
    due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=None)
    completed_date = models.DateField(blank=True, null=True)
    assigned_by = models.ForeignKey(TodoUser, related_name='todo_created_by')
    assigned_to = models.ForeignKey(TodoUser, blank=True, null=True, related_name='todo_assigned_to')

    def __str__(self):
        return self.title

    def save(self):
        if self.completed:
            self.completed_date = datetime.datetime.now
        super(Item, self).save()
