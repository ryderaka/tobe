from django.contrib import admin
from .models import TodoUser, TodoList#, TodoStatus

admin.site.register(TodoUser)
admin.site.register(TodoList)
# admin.site.register(TodoStatus)
