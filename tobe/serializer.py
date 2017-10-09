# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import TodoList


class TodoTaskSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(many=True)
    # description = serializers.CharField(many=True)
    # created_by = serializers.IntegerField(many=True)
    # created_date = serializers.DateTimeField(many=True)
    # assigned_to = serializers.IntegerField(many=True)
    # assigned_date = serializers.DateTimeField(many=True)
    # due_date = serializers.DateTimeField(many=True)
    # isaccepted = serializers.BooleanField(many=True)

    class Meta:
        model = TodoList
        fields = (
            'title',
            'description',
        )
